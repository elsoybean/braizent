---
name: import-recipe
description: Import a recipe from a URL into the meal-planning collection via the GitHub connector, and generate its Cooklang .cook file.
---

# Import Recipe (Desktop)

Bring a recipe from a URL into the user's `elsoybean/meal-planning` repo through the GitHub connector.

## Fetch and standardize

Fetch the page, preferring structured data (JSON-LD / schema.org) and falling back to parsing the content. Convert to the house standard: metric, **grams by weight**; numbered steps with temperatures in °C; a short description; source name + URL; sensible tags. Title is comma-inverted, lead-noun-first ("Chicken Thighs, Crispy Soy-Glazed"). Respect the profile's constraints (no anise/licorice). Structure the ingredients as discrete fields — quantity, unit, item, prep — since that's what the saver needs.

## Save — hand to the save contract

Assemble the standardized recipe as a structured object (`kind: standard`; `ingredients` as { quantity, unit, item, prep }; `steps`; `source` { name, url }; `tags`; `description`) and follow the **recipe-save contract** (`_recipe-saver.md`, bundled in this skill folder). It derives the slug, writes `recipes/<slug>/<slug>.md` and `cook/<slug>.cook` at the right paths, won't overwrite, and commits. Don't re-derive the slug, paths, or format here — just hand over clean structured data and confirm before it writes.
