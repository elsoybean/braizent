---
name: build-profile
description: Create or update the user's PROFILE.md, and regenerate the CookCLI store-routing and pantry configs from it.
---

# Build Profile

Capture the user's cooking context in `PROFILE.md` — the human-readable source the other skills read. Two modes: create from scratch, or update a section. Keep it readable prose-and-bullets, not a form dump; the user should be comfortable hand-editing it.

## Cover these dimensions

Household and servings (day-of-week variance, appetite, leftovers); taste (cuisines, loves, dislikes-not-allergies, spice tolerance, adventurousness); **dietary restrictions**; shopping (stores and routing — see below); pantry staples; cooking style (skill, weekday/weekend time, equipment, standard seasoning blend, saved fats, meal-prep appetite); and optionally health goals and budget. Interview only what's needed — infer and confirm rather than interrogating, and on an update just touch the named section.

## Dietary restrictions — handle with care

This is a safety section, so be precise. If someone says "allergic," ask whether it's a medical reaction or a strong dislike, and record the severity plainly: SEVERE ALLERGY / ALLERGY / SENSITIVITY / INTOLERANCE versus PREFERENCE (taste, religious, ethical). Read every restriction back to confirm. Never offer medical advice; keep to the food implications and point health questions to their doctor. "None reported" is a fine answer.

## Shopping and pantry feed the CookCLI configs

These two sections are the source for the cooking layer's config, so capture them structured enough to regenerate cleanly:

- **Store routing** — the channels the user shops (e.g. Knuspr online by default, Rewe in person, an Asian market, hand-pick for premium cuts) and which items or categories go to each, including aliases for things named differently across recipes.
- **Pantry staples** — what's always on hand (so it drops off shopping lists). Note the deliberate exception: fast-moving basics the user wants to keep buying (e.g. rice, pasta) stay OFF the always-have list so they still appear.

After writing or updating either section, **regenerate the configs from the profile**:

- `cook/config/aisle.conf` — one `[section]` per store channel, its items one per line with `|` aliases, in the profile's stated order.
- `cook/config/pantry.conf` — the staples as entries under sensible location groups, omitting the fast-movers above.

These live in `cook/config/`, CookCLI's config directory. `PROFILE.md` is the source of truth and the configs are generated from it, so edits go to the profile and then regenerate — not the other way around.

## Write and confirm

Write or update `PROFILE.md` as readable markdown with a clear section per dimension and a Last-updated date; on updates, edit just the changed sections and bump the date. Validate that the dietary section carries severity markers and a warning header. Summarize what changed, and note if the configs were regenerated.
