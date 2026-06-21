"""Core recommendation logic — prompt construction and LLM interaction."""

from openai import AsyncOpenAI

from recipe_recommender.config import (
    DEFAULT_MODEL,
    OLLAMA_API_KEY,
    OLLAMA_BASE_URL,
    SYSTEM_PROMPT,
)
from recipe_recommender.models import RecipeRecommendations, RecipeRequest


def build_user_prompt(request: RecipeRequest) -> str:
    """Construct the user-facing prompt from a RecipeRequest."""
    parts: list[str] = [
        f"Available ingredients: {', '.join(request.ingredients)}.",
        f"Please suggest {request.count} recipe(s).",
    ]

    if request.dietary_restrictions:
        restrictions = ", ".join(request.dietary_restrictions)
        parts.append(f"Dietary restrictions: {restrictions}.")

    if request.cuisine_preference:
        parts.append(f"Preferred cuisine: {request.cuisine_preference}.")

    if request.max_time_minutes is not None:
        parts.append(f"Maximum total time (prep + cook): {request.max_time_minutes} minutes.")

    return " ".join(parts)


async def recommend_recipes(
    request: RecipeRequest,
    model_name: str = DEFAULT_MODEL,
) -> RecipeRecommendations:
    """Call Ollama with grammar-constrained JSON output and validate with Pydantic.

    Uses response_format with the full JSON schema so Ollama constrains generation
    at the grammar level — more reliable than tool calls with local models.
    """
    client = AsyncOpenAI(base_url=OLLAMA_BASE_URL, api_key=OLLAMA_API_KEY)

    response = await client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": build_user_prompt(request)},
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "recipe_recommendations",
                "schema": RecipeRecommendations.model_json_schema(),
            },
        },
    )

    content = response.choices[0].message.content
    if not content:
        raise RuntimeError("Model returned an empty response")

    return RecipeRecommendations.model_validate_json(content)
