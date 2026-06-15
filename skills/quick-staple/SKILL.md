---
name: quick-staple
description: Capture a familiar recipe you make regularly as a flexible memory aid, profile-aware.
---

# Quick Staple

Document a recipe the user makes from memory — flexible, mostly on-hand ingredients, easy to vary. The point is a meal-planning reminder and shopping cue, not precise instructions.

## Be profile-aware first

Read `PROFILE.md` so you can make assumptions instead of interrogating: household size and servings, standard seasoning blend, saved fats and pantry staples, store routing (e.g. Pollofino from Knuspr), dietary needs. If the user says "my usual blend" or "seasoned normally," use what the profile defines rather than asking.

## Capture

Have the user describe the dish in a sentence or two, then fill gaps conversationally — only what the profile can't already tell you. Variations and "why it's a go-to" are worth asking; basic seasoning usually isn't. Keep it quick; they know how to cook this.

## Conventions

- **Name / slug** — house convention: lead with the dish, modifiers after a comma ("Chicken Thighs, Pan-Fried with Dirty Rice"); slug is that lowercased and hyphenated. Saved at `recipes/[slug]/[slug].md`.
- **Format** — the quick-staple shape, not a precise recipe: a header with `**Type:** Quick Staple`, then Description, Core Components (with variation notes), Shopping Needs (usually-buy vs. always-have, drawing on the profile's pantry), high-level Preparation Notes (memory joggers, not step-by-step), Variation Ideas, and a `[quick-staple]` tag plus a few more.
- Keep amounts loose — to-taste, not weighed.

## No .cook (by design)

Quick staples have no measurable quantities, so they stay out of `cook/` — `to-cooklang` skips anything tagged `[quick-staple]`. When the user wants one cookable (to share, or to put on the kitchen server), use `recipe-variant` to make a `_precise` version; that variant is what gets a `.cook`.

## Finish

Confirm the name, link the file, and note it's tagged `[quick-staple]` for meal planning.
