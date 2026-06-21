"""Constants and settings for the recipe recommender."""

OLLAMA_BASE_URL: str = "http://localhost:11434/v1"
OLLAMA_API_KEY: str = "ollama"

DEFAULT_MODEL: str = "llama3.1:8b"
DEFAULT_RECIPE_COUNT: int = 3
MAX_RECIPE_COUNT: int = 10

SYSTEM_PROMPT: str = (
    "You are a professional chef and recipe expert. "
    "Given a list of available ingredients and user constraints, "
    "suggest creative, practical recipes that can realistically be made. "
    "Return only recipes that use a significant portion of the provided ingredients. "
    "Be specific with quantities, steps, and timings."
)
