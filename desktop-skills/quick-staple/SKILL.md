---
name: quick-staple
description: Capture a from-memory regular as a flexible memory aid, saved to the meal-planning collection via the GitHub connector. Profile-aware; no precise amounts.
---

# Quick Staple (Desktop)

Document a recipe the user makes from memory — flexible, mostly on-hand, easy to vary — saved to `elsoybean/meal-planning` via the GitHub connector.

## Profile-aware capture

Read `PROFILE.md` (connector) so you can assume rather than interrogate: servings, standard seasoning blend, saved fats and pantry staples, store routing, dietary needs (no anise/licorice). Have the user describe the dish in a sentence or two; fill only the gaps the profile can't. Variations and "why it's a go-to" are worth asking; basic seasoning isn't. Keep it quick — they know how to cook this.

## Save (connector)

Write `recipes/[slug]/[slug].md` (house lead-noun-first naming) in the quick-staple shape: a header with `**Type:** Quick Staple`, then Description, Core Components (with variation notes), Shopping Needs (usually-buy vs. always-have, drawing on the profile's pantry), high-level Preparation Notes (memory joggers, not step-by-step), Variation Ideas, and a `[quick-staple]` tag. Amounts stay loose — to-taste, not weighed.

## No .cook

Quick staples stay out of `cook/` (no measurable quantities). To make one cookable later, use `recipe-variant` to create a `_precise` version — that variant gets the `.cook`. Confirm, then link the file.
