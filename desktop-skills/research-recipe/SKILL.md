---
name: research-recipe
description: Deeply research a dish across many sources (simple, authentic, refined, regional, food-science), synthesize what defines it, then develop and save the user's own version to the meal-planning collection via the GitHub connector, with its .cook and full sourcing.
---

# Research Recipe (Desktop)

This is the deep one. The goal is not a recipe lifted from a single page — it's a real understanding of a dish, built from many sources, then a version developed *with* the user that reflects that understanding and their kitchen. Do the thorough version every time; if a run only skimmed a page or two, it failed.

## 1. Profile first

Read `PROFILE.md` from `elsoybean/meal-planning` (GitHub connector): household size and servings, dietary restrictions (**no anise/licorice** — star anise, fennel seed, five-spice), skill level, equipment, region and shopping, pantry. This shapes both what you research and how you adapt it.

## 2. Research widely — several sources per angle, in parallel

Fire multiple web searches at once; never settle for the first result. Gather at least these angles, each from more than one source:

- **Authentic / traditional** — *prioritize voices from the dish's own culture*, especially first-generation immigrants and people writing about their family's cooking. Capture the traditional method, the ingredients that matter and why, regional variations, and the dish's history and significance. This angle carries the most weight.
- **Simple / weeknight** — the pared-back home version: what gets cut, and what stays non-negotiable even when simplifying.
- **Refined / chef** — a restaurant or serious-cook treatment: the advanced technique and precision, what they do that home versions don't.
- **Food science / technique** — when the dish hinges on a mechanism (emulsion, gelatinization, fermentation, Maillard, dough hydration), get the *why* from a reliable source (Kenji / Serious Eats, Cook's Illustrated, food-science writing). Don't hand-wave it.

From each source pull: ingredients and rough ratios, technique and sequence, the reasoning, and what makes that version distinctive. Track where sources agree and where they contradict each other.

## 3. Synthesize — show the user the landscape

Before proposing anything, lay out:

- **The soul of the dish** — what every credible version shares; the things you can't change without making it a different dish.
- **Where versions diverge** — ingredients, technique, timing — and *why* (tradition, convenience, refinement, regional identity).
- **Cultural context** — history and significance, handled with respect. If the user wants to change something traditional, make sure they understand what they're changing and what it means, then back their choice.

This synthesis is the part that makes the skill worth running — don't skip it to get to a recipe faster.

## 4. Develop the user's version *with* them

Don't jump to a finished recipe. Talk through the real decisions: which angle to anchor on, time and effort budget, authenticity vs. accessibility, equipment, substitutions for the profile. Propose a path, get reactions, iterate. Fold in the elevation steps that genuinely matter (bloom spices/miso in fat, toast, temper, rest, velvet) where they earn their place. Adapt fully to the profile — servings, equipment, metric by weight (grams).

## 5. Save — hand to the save contract

You've done the judgment; the writing is mechanical, so don't re-derive it. Assemble the results as structured recipe objects and run the **recipe-save contract** (`desktop-skills/_recipe-saver.md` in the braizent repo — read it once via the connector):

- the user's version as `kind: standard`, carrying `development_notes` and `research_sources`,
- each notable source version as `kind: reference-variant` (the contract keeps these markdown-only).

The contract handles slugs, paths, the `.md`/`.cook` rendering, never-overwriting, and the commit. Then link everything and recap what makes the user's version theirs.

## The bar

A good run: searches several real sources across the angles, surfaces genuine disagreement between them, teaches the user something they didn't know (history, technique, the *why*), and lands on a recipe that's clearly grounded and clearly theirs. One or two pages and no synthesis is not this skill — it's just a web search.
