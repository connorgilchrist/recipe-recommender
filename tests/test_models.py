"""Tests for data models."""

import pytest

from recipe_recommender.models import Recipe, RecipeIngredient, RecipeRecommendations, RecipeRequest


def test_recipe_request_defaults() -> None:
    request = RecipeRequest(ingredients=["chicken", "garlic"])
    assert request.dietary_restrictions == []
    assert request.cuisine_preference is None
    assert request.max_time_minutes is None
    assert request.count == 3


def test_recipe_request_full() -> None:
    request = RecipeRequest(
        ingredients=["salmon", "lemon", "dill"],
        dietary_restrictions=["gluten-free"],
        cuisine_preference="Scandinavian",
        max_time_minutes=30,
        count=2,
    )
    assert len(request.ingredients) == 3
    assert request.max_time_minutes == 30


def test_recipe_model_validation() -> None:
    recipe = Recipe(
        name="Garlic Chicken",
        description="Simple pan-fried chicken with garlic.",
        cuisine="European",
        ingredients=[RecipeIngredient(name="chicken breast", quantity="2 pieces")],
        steps=["Season chicken.", "Pan-fry until golden."],
        prep_time_minutes=5,
        cook_time_minutes=15,
        servings=2,
    )
    assert recipe.name == "Garlic Chicken"
    assert len(recipe.steps) == 2


def test_recipe_recommendations_wraps_list() -> None:
    rec = RecipeRecommendations(
        recipes=[
            Recipe(
                name="Test",
                description="desc",
                cuisine="Any",
                ingredients=[],
                steps=["step"],
                prep_time_minutes=1,
                cook_time_minutes=1,
                servings=1,
            )
        ]
    )
    assert len(rec.recipes) == 1
