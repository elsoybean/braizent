---
name: quick-staple
description: Capture a from-memory regular as a flexible memory aid, saved to the meal-planning collection via the GitHub connector. Profile-aware; no precise amounts.
---

# Quick Staple (Desktop)

Document a recipe the user makes from memory — flexible, mostly on-hand, easy to vary — saved to `elsoybean/meal-planning` via the GitHub connector.

## Profile-aware capture

Read `PROFILE.md` (connector) so you can assume rather than interrogate: servings, standard seasoning blend, saved fats and pantry staples, store routing, dietary needs (no anise/licorice). Have the user describe the dish in a sentence or two; fill only the gaps the profile can't. Variations and "why it's a go-to" are worth asking; basic seasoning isn't. Keep it quick — they know how to cook this.

## Save — hand to the save contract

Assemble the staple as a structured object with `kind: quick-staple` — loose core components, shopping needs, high-level prep notes, and variation ideas, with no weighed amounts. Follow the **recipe-save contract** (`_recipe-saver.md`, bundled in this skill folder). It writes `recipes/<slug>/<slug>.md` in the quick-staple shape and — correctly — no `.cook`. To make one cookable later, `recipe-variant` with a `_precise` suffix produces the version that does get a `.cook`.
