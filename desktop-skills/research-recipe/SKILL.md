---
name: research-recipe
description: Research a dish across sources (simple / authentic / refined), develop the user's version, and save it to the meal-planning collection via the GitHub connector with its .cook.
---

# Research Recipe (Desktop)

Research a dish from several angles, develop the user's version together, and save it to `elsoybean/meal-planning` through the GitHub connector.

## Profile first

Read `PROFILE.md` (connector) for household size, restrictions (no anise/licorice), skill, equipment, region, and pantry.

## Research at least three angles (web)

- **Simple** — minimal, weeknight home-cook version.
- **Authentic** — traditional method. Prioritize voices from the dish's own culture, especially first-generation immigrants; capture the context and history, not just the steps. Respect the dish's significance; if the user wants to change something traditional, help them understand what they're changing.
- **Refined** — a chef or restaurant version with advanced technique.

Add regional or modern angles where they teach something.

## Synthesize, then develop together

Lay out the non-negotiable core, how the versions differ (ingredients, technique, timing), and the cultural context. Collaborate on the user's version — which angle, time budget, authenticity vs. accessibility, adaptations — adapted to the profile (servings, equipment, metric/grams). Iterate on feedback before saving.

## Save (connector)

- `recipes/[slug]/[slug].md` — the user's version, standard format, with a short Development Notes line and a **Research Sources** list (URLs). Always credit the sources.
- `recipes/[slug]/[slug]_simple.md`, `_authentic.md`, `_refined.md` — the source versions (metric, standard layout, a note on what each teaches), markdown-only.
- `cook/[slug].cook` — the main recipe's Cooklang (text). The reference variants don't get `.cook` files.

Slug uses the house lead-noun-first convention. Confirm before committing; link what you saved.
