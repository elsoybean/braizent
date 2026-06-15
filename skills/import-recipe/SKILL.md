---
name: import-recipe
description: Import a recipe from a URL into a markdown file in the collection, then generate its Cooklang version.
---

# Import Recipe

Fetch a recipe from a URL, save it as a standard recipe in `recipes/`, then generate its `.cook` counterpart so it's immediately cookable.

## Input

A recipe URL. If none was given, ask for it.

## Fetch

WebFetch the page and extract the recipe: title, description, source, cuisine, category, servings, total/active time, ingredients (quantity, unit, prep), instructions, temperatures, and any notable tips. Prefer structured data (JSON-LD / schema.org Recipe) and fall back to the page HTML.

## Conventions to apply

- **Title** — lead with the dish, modifiers after a comma: "Classic Lasagna" → "Lasagna, Classic"; "Creamy Leek and Potato Soup" → "Leek and Potato Soup, Creamy". A bare name ("Minestrone") stays as-is. This ordering is the house convention across the whole collection.
- **Slug and paths** — title lowercased, spaces to hyphens, alphanumerics only: "Lasagna, Classic" → `lasagna-classic`, saved at `recipes/[slug]/[slug].md`.
- **Metric** — weight in g/kg, volume in ml, temperatures in °C. Chris cooks by weight, so prefer grams for anything you would weigh; keep count units (cloves, whole) as-is.
- **Tags** — 5–10 lowercase, hyphenated tags across main ingredients, cuisine, category, method, and (only if clearly true) dietary/time attributes.

## Output

Write `recipes/[slug]/[slug].md` in the collection's standard shape:

```markdown
# [Title]

**Source:** [name]
**URL:** [url]
**Cuisine:** [cuisine]
**Category:** [category]
**Servings:** [n]
**Total Time:** [time]
**Active Time:** [time, if known]

## Description
[short description]

## Ingredients

| Quantity | Unit | Ingredient | Preparation |
|----------|------|------------|-------------|
| ... | ... | ... | ... |

## Instructions
1. ...

## Notes from Source
- [tips from the original, or leave empty]

## Personal Notes
-

## Tags
[tag] [tag] [tag]
```

The four-column ingredient table is a contract that `to-cooklang` and `recipe-card` depend on — keep that structure. Use "-" for the quantity/unit of to-taste items; leave Preparation blank when unspecified.

## Then generate the .cook

Run the `to-cooklang` skill for the new recipe so `cook/[slug].cook` is created and it appears in CookCLI. It transcribes the table faithfully and won't overwrite an existing `.cook`.

## Finish

Confirm the title, link the saved markdown, and note the `.cook` was generated.
