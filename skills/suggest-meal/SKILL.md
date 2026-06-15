---
name: suggest-meal
description: Suggest a complete meal (main + sides) for a given date, drawing on the collection first, then the web.
---

# Suggest Meal

Suggest a single complete meal for a date — main plus sides — fitting the user's profile, schedule, and what's on hand.

## Set the date and context

- **Verify the date with the system `date` command** (don't do calendar math in your head); confirm the day with the user.
- Check `meal-plans/*.md` for that date — if something's already planned, offer to keep or swap it.
- Read `PROFILE.md` (household size, dietary restrictions — never violate, cuisines, skill, equipment, recurring guests, pantry).
- Ask only what you still need: which meal, how many, leftovers or not, time available, anything to use up. Keep it brief.

## Find the main

Search the collection first (`recipes/`, and the `cook/` layer) by time, tags, cuisine, and ingredients, excluding anything restricted and what they just ate. If nothing fits well, search the web for a few strong options from reputable sources that match their from-scratch, no-shortcuts style, and offer to bring the chosen one in via `import-recipe` (or `research-recipe` for a deeper dive). Present a few options with a clear recommendation and why.

## Round it out

Suggest sides that complement the main and fit the time — often just a vegetable and a starch, or note it's already a complete meal. Prefer simple sides (oil/salt/roast) unless they have side recipes; offer to save a good one as a `quick-staple`.

## Land it

Present the full meal for approval and iterate on feedback. On approval, offer to add it to the meal plan (edit the existing plan file or start one). For shopping, add the chosen recipe to the CookCLI list so it flows to Bring (see `add-to-shopping-list`) rather than writing out an ingredient list.
