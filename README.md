# Recipe Recommender

Suggests recipes based on available ingredients and cooking constraints. Uses a local LLM via Ollama to return **structured, validated Python objects** — not free text.

**Skill demonstrated:** Structured LLM output with [Pydantic AI](https://ai.pydantic.dev)

## Stack

| Component | Tool |
|---|---|
| LLM inference | Ollama (local, MPS-accelerated) |
| Structured output | Pydantic AI |
| CLI | Click + Rich |

## Setup

```bash
# Pull the model
ollama pull llama3.1:8b

# Install dependencies
uv sync
```

## Usage

```bash
# Basic — three ingredients, default 3 recipes
uv run recipe-recommender -i chicken -i garlic -i lemon

# With constraints
uv run recipe-recommender \
  -i tofu -i broccoli -i "soy sauce" \
  --dietary vegetarian \
  --cuisine Asian \
  --time 30 \
  --count 2

# Use a different model
uv run recipe-recommender -i salmon -i dill --model gemma3:12b
```

### Options

| Flag | Short | Description |
|---|---|---|
| `--ingredient` | `-i` | Available ingredient (repeat for multiple) |
| `--dietary` | `-d` | Dietary restriction, e.g. `vegetarian` (repeat for multiple) |
| `--cuisine` | `-c` | Preferred cuisine style |
| `--time` | `-t` | Max total time in minutes |
| `--count` | `-n` | Number of recipes to suggest (1–10, default 3) |
| `--model` | `-m` | Ollama model name (default `llama3.1:8b`) |

## Project Structure

```
recipe_recommender/
├── config.py       — constants: model name, Ollama URL, system prompt
├── models.py       — RecipeRequest (dataclass), Recipe / RecipeRecommendations (Pydantic)
├── recommend.py    — prompt construction and Pydantic AI agent
└── cli.py          — Click command and Rich display
tests/
├── test_models.py
└── test_recommend.py
```

## Tests

```bash
uv run pytest
```
