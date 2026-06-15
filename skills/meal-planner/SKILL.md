---
name: meal-planner
description: Build a personalized, profile- and leftover-aware meal plan, and feed the week's recipes into the CookCLI -> Bring shopping flow.
---

# Meal Planner

Plan meals for a period that fit the user's life, then route the week's recipes into shopping. Collaborative and realistic — the aim is a plan they're glad to cook.

## Ground the plan

- Read `PROFILE.md`: household size and appetite, dietary restrictions (never violate), cuisines and skill, equipment, shopping and store patterns, pantry, recurring events (e.g. Wednesday guests), standard seasonings.
- **Verify dates with the system `date` command** — don't do calendar math in your head. Confirm the period with the user.
- Skim the recent `meal-plans/*.md` to avoid repeating last week's dishes and to spot leftover ingredients worth using.

## Gather intent

Ask about the things that actually shape a week: which meals to plan, busy vs. relaxed nights, any theme, one or two featured dishes to build around, ingredients to use up, guests or nights out. Don't over-survey — take what they give and infer the rest from the profile.

## Pick the meals

Work chronologically (so you can track what's been opened and what's leftover) and use `suggest-meal` for each slot with rich context so it needs to ask little. Get the user's approval per meal, and balance protein, cuisine, and effort across the week — staples on busy nights, the featured dish where there's time.

## Write the plan

Create `meal-plans/[YYYY-MM-DD] to [YYYY-MM-DD].md`: a short overview of the week's strategy, a day-by-day schedule (each main linked to its recipe, with simple sides and rough timing), an ingredient-efficiency note (what carries across meals), a light prep schedule, and an empty feedback section. Link recipes in `recipes/` (or their `cook/` files).

## Shopping

Don't embed a shopping list. Put the week's recipes onto the CookCLI shopping list (see `add-to-shopping-list`) so CookCLI + `bring-sync` push the aggregated, pantry-trimmed, channel-routed items into the shared Bring! list. One-offs go straight into Bring. Point the user there rather than writing a list into the plan.

## Finish

Summarize the week, the featured dish, and where shopping lives (Bring), and remind them they can swap any meal via `suggest-meal`.
