---
name: recipe-variant
description: Create a variant of a collection recipe (precise, dietary, scaled, method change) and save it alongside the original via the GitHub connector, with its own .cook.
---

# Recipe Variant (Desktop)

Make a variant of an existing recipe in `elsoybean/meal-planning` and save it through the GitHub connector.

## Work from the original

Read the source recipe (connector). Clarify the goal: a `_precise` version of a quick staple (for sharing or cooking), a dietary adaptation (`_vegetarian` / `_vegan` / `_gluten-free`), a scale (`_double`), a method change (`_grilled` / `_instant-pot`), or anything else. Adapt thoughtfully — substitutions and technique changes grounded in real cooking (search to verify when unsure), profile-aware, metric/grams, no anise/licorice. Structure the result as discrete ingredient fields (quantity, unit, item, prep) and steps.

## Save — hand to the save contract

Assemble the variant as a structured object with `kind: variant`, `base_slug` (the original's slug) and `suffix` (e.g. `vegetarian`, `double`, `precise`), plus the ingredients and steps. (If the variant is itself a loose quick staple, use `kind: quick-staple` instead.) Run the **recipe-save contract** (`desktop-skills/_recipe-saver.md`, via the connector): it writes the variant beside the original, adds its `.cook` (variants get one; quick-staples don't), links back to the original, won't overwrite, and commits. Don't re-derive the paths or format.
