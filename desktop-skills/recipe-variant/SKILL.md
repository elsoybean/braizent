---
name: recipe-variant
description: Create a variant of a collection recipe (precise, dietary, scaled, method change) and save it alongside the original via the GitHub connector, with its own .cook.
---

# Recipe Variant (Desktop)

Make a variant of an existing recipe in `elsoybean/meal-planning` and save it through the GitHub connector.

## Work from the original

Read the source recipe (connector). Clarify the goal: a `_precise` version of a quick staple (for sharing or cooking), a dietary adaptation (`_vegetarian` / `_vegan` / `_gluten-free`), a scale (`_double`), a method change (`_grilled` / `_instant-pot`), or anything else. Adapt thoughtfully — substitutions and technique changes grounded in real cooking (search to verify when unsure), profile-aware, metric/grams, no anise/licorice.

## Save (connector)

- `recipes/[slug]/[slug]_[suffix].md` — the variant, in the same folder as the original, in the right format (standard recipe, or quick-staple shape if that's what it is). Link back to the original in Personal Notes.
- `cook/[slug]_[suffix].cook` — its Cooklang (text), unless the variant is itself a quick staple with no real measurements.

Confirm before committing; link the files.
