---
name: import-recipe
description: Import a recipe from a URL into the meal-planning collection via the GitHub connector, and generate its Cooklang .cook file.
---

# Import Recipe (Desktop)

Bring a recipe from a URL into the user's `elsoybean/meal-planning` repo through the GitHub connector.

## Fetch and standardize

Fetch the page, preferring structured data (JSON-LD / schema.org) and falling back to parsing the content. Convert to the house standard: metric, **grams by weight**; a four-column ingredient table (Quantity | Unit | Ingredient | Preparation); numbered steps with temperatures in °C; a short description; source name + URL; sensible tags. Title and slug follow the house convention — lead with the dish, modifiers after a comma ("Chicken Thighs, Crispy Soy-Glazed"), slug lowercased and hyphenated. Respect the profile's constraints (no anise/licorice).

## Write to the repo (connector)

Commit to `elsoybean/meal-planning`:

- `recipes/[slug]/[slug].md` — the standardized recipe.
- `cook/[slug].cook` — the Cooklang version, written as text (no `cook` binary needed): YAML frontmatter (`title`, `servings`, `cuisine`, `course`, `time`, `source`, `tags`); body with `@ingredient{qty%unit}`, `#cookware{}`, `~{timer}`, and `== Section ==` headers; `=` to lock to-taste amounts from scaling. Don't overwrite an existing `.cook`.

Confirm before committing, then link the files.
