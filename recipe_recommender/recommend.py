"""Core recommendation logic — prompt construction and LLM interaction."""

from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

from recipe_recommender.config import (
    DEFAULT_MODEL,
    OLLAMA_API_KEY,
    OLLAMA_BASE_URL,
    OUTPUT_RETRIES,
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


def build_agent(model_name: str = DEFAULT_MODEL) -> Agent[None, RecipeRecommendations]:
    """Create a Pydantic AI agent configured for Ollama."""
    model = OpenAIModel(
        model_name,
        provider=OpenAIProvider(base_url=OLLAMA_BASE_URL, api_key=OLLAMA_API_KEY),
    )
    return Agent(
        model,
        output_type=RecipeRecommendations,
        system_prompt=SYSTEM_PROMPT,
        retries=OUTPUT_RETRIES,
    )


async def recommend_recipes(
    request: RecipeRequest,
    agent: Agent[None, RecipeRecommendations],
) -> RecipeRecommendations:
    """Run the agent and return validated recipe recommendations."""
    prompt = build_user_prompt(request)
    result = await agent.run(prompt)
    return result.output
