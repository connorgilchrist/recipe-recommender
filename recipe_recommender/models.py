"""Data models for recipe recommendation requests and responses."""

from dataclasses import dataclass, field

from pydantic import BaseModel, Field


@dataclass
class RecipeRequest:
    """User's available ingredients and cooking constraints."""

    ingredients: list[str]
    dietary_restrictions: list[str] = field(default_factory=list)
    cuisine_preference: str | None = None
    max_time_minutes: int | None = None
    count: int = 3


class RecipeIngredient(BaseModel):
    """A single ingredient with name and quantity."""

    name: str
    quantity: str = Field(description="e.g. '2 cloves', '200g', '1 tbsp'")


class Recipe(BaseModel):
    """A complete recipe with ingredients and step-by-step instructions."""

    name: str
    description: str = Field(description="One or two sentence summary of the dish")
    cuisine: str = Field(description="e.g. Italian, Thai, Mexican")
    ingredients: list[RecipeIngredient]
    steps: list[str] = Field(description="Ordered list of cooking instructions")
    prep_time_minutes: int
    cook_time_minutes: int
    servings: int


class RecipeRecommendations(BaseModel):
    """Structured output from the LLM — a list of recommended recipes."""

    recipes: list[Recipe]
