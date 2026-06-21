"""CLI entry point for the recipe recommender."""

import asyncio

import click
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from recipe_recommender.config import DEFAULT_MODEL, DEFAULT_RECIPE_COUNT, MAX_RECIPE_COUNT
from recipe_recommender.models import Recipe, RecipeRequest
from recipe_recommender.recommend import build_agent, recommend_recipes

console = Console()


def _render_recipe(recipe: Recipe, index: int) -> Panel:
    """Format a single recipe as a Rich panel."""
    body = Text()

    body.append(f"{recipe.description}\n\n", style="italic")
    body.append(
        f"Cuisine: {recipe.cuisine}  |  "
        f"Prep: {recipe.prep_time_minutes}m  |  "
        f"Cook: {recipe.cook_time_minutes}m  |  "
        f"Serves: {recipe.servings}\n\n",
        style="dim",
    )

    body.append("Ingredients\n", style="bold")
    for ing in recipe.ingredients:
        body.append(f"  • {ing.quantity} {ing.name}\n")

    body.append("\nMethod\n", style="bold")
    for i, step in enumerate(recipe.steps, start=1):
        body.append(f"  {i}. {step}\n")

    return Panel(body, title=f"[bold cyan]{index}. {recipe.name}[/bold cyan]", expand=False)


@click.command()
@click.option(
    "--ingredient",
    "-i",
    "ingredients",
    multiple=True,
    required=True,
    help="An available ingredient (repeat for multiple).",
)
@click.option(
    "--dietary",
    "-d",
    "dietary_restrictions",
    multiple=True,
    help="A dietary restriction e.g. vegetarian, gluten-free (repeat for multiple).",
)
@click.option("--cuisine", "-c", default=None, help="Preferred cuisine style.")
@click.option("--time", "-t", "max_time_minutes", default=None, type=int, help="Max total time in minutes.")
@click.option(
    "--count",
    "-n",
    default=DEFAULT_RECIPE_COUNT,
    show_default=True,
    type=click.IntRange(1, MAX_RECIPE_COUNT),
    help="Number of recipes to suggest.",
)
@click.option("--model", "-m", default=DEFAULT_MODEL, show_default=True, help="Ollama model name.")
def recommend(
    ingredients: tuple[str, ...],
    dietary_restrictions: tuple[str, ...],
    cuisine: str | None,
    max_time_minutes: int | None,
    count: int,
    model: str,
) -> None:
    """Suggest recipes based on available ingredients and constraints."""
    request = RecipeRequest(
        ingredients=list(ingredients),
        dietary_restrictions=list(dietary_restrictions),
        cuisine_preference=cuisine,
        max_time_minutes=max_time_minutes,
        count=count,
    )

    agent = build_agent(model)

    console.print(f"\n[bold]Finding {count} recipe(s) using {model}…[/bold]\n")

    try:
        recommendations = asyncio.run(recommend_recipes(request, agent))
    except Exception as exc:
        raise click.ClickException(str(exc)) from exc

    for i, recipe in enumerate(recommendations.recipes, start=1):
        console.print(_render_recipe(recipe, i))
        console.print()
