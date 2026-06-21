"""Tests for prompt construction logic."""

import pytest

from recipe_recommender.models import RecipeRequest
from recipe_recommender.recommend import build_user_prompt


def test_prompt_contains_ingredients() -> None:
    request = RecipeRequest(ingredients=["chicken", "garlic", "lemon"])
    prompt = build_user_prompt(request)
    assert "chicken" in prompt
    assert "garlic" in prompt
    assert "lemon" in prompt


def test_prompt_includes_count() -> None:
    request = RecipeRequest(ingredients=["pasta"], count=5)
    prompt = build_user_prompt(request)
    assert "5 recipe(s)" in prompt


def test_prompt_includes_dietary_restrictions() -> None:
    request = RecipeRequest(ingredients=["tofu"], dietary_restrictions=["vegan", "gluten-free"])
    prompt = build_user_prompt(request)
    assert "vegan" in prompt
    assert "gluten-free" in prompt


def test_prompt_includes_cuisine() -> None:
    request = RecipeRequest(ingredients=["rice"], cuisine_preference="Japanese")
    prompt = build_user_prompt(request)
    assert "Japanese" in prompt


def test_prompt_includes_time_constraint() -> None:
    request = RecipeRequest(ingredients=["eggs"], max_time_minutes=20)
    prompt = build_user_prompt(request)
    assert "20 minutes" in prompt


def test_prompt_omits_optional_fields_when_absent() -> None:
    request = RecipeRequest(ingredients=["butter"])
    prompt = build_user_prompt(request)
    assert "Dietary" not in prompt
    assert "cuisine" not in prompt.lower() or "Preferred cuisine" not in prompt
    assert "Maximum total time" not in prompt
