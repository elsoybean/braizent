---
name: research-recipe
description: Research a dish from multiple sources (simple, authentic, refined), then develop and save a personalized version with its Cooklang file; keep the research variants for reference.
---

# Research Recipe

Research a dish from several angles, then collaborate with the user to develop their own version — saved as a standard recipe, made cookable, with the source versions preserved for reference.

## Profile first

Read `PROFILE.md` for household size, restrictions, skill, equipment, region, and pantry — this shapes both the research and the final recipe.

## Research at least three angles

Use WebSearch/WebFetch (in parallel) to gather distinct versions:

- **Simple** — minimal ingredients, weeknight-friendly home-cook version.
- **Authentic** — traditional method. **Prioritize voices from the dish's own culture, especially first-generation immigrants sharing family recipes.** Capture the cultural context and history, not just the steps. Respect the dish's significance; if the user wants to change something traditional, help them understand what they're changing.
- **Refined** — a chef or restaurant version with advanced technique.

Add regional or modern angles where they teach something.

## Synthesize and present

Briefly lay out what's essential across all versions (the non-negotiable soul of the dish), how they differ (ingredients, technique, timing), and the cultural context. Then collaborate with the user on their version — which angle they lean toward, their time budget, authenticity vs. accessibility, any adaptations. Ask a few real questions; don't over-survey.

## Develop their version

Build the user's recipe from the angle that fits, borrowing across the others, adapted to their profile (servings, equipment, metric — grams by weight). Explain the key choices. Iterate on their feedback before saving.

## Save

- **Main recipe** → `recipes/[slug]/[slug].md` in standard format (slug follows the house lead-noun-first convention), including a short Development Notes line and a **Research Sources** list with URLs. **Always credit the sources** — it's ethical and lets the user explore the originals.
- **Reference variants** → `recipes/[slug]/[slug]_simple.md`, `_authentic.md`, `_refined.md`, each the source version (metric, standard layout) with a note on what it teaches. These are reference, so they stay markdown-only.
- Then run `to-cooklang` for the **main** recipe so `cook/[slug].cook` exists. The reference variants don't get `.cook` files.

## Finish

Link the main recipe and the variants, recap what makes the user's version theirs, and keep the source credits visible.
