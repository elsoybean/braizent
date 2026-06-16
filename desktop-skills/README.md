# Desktop skills

Versions of the braizent skills adapted for the **consumer Claude apps** (web / desktop / mobile), as opposed to the Claude Code plugin in `../skills/`. These let you work with the recipe collection while chatting with Claude from your phone or laptop.

## How these differ from the Code skills

The Code skills assume a local checkout of the meal-planning repo, the `cook` binary on PATH, and local file tools (Read/Write/Grep). Claude Desktop runs in Claude's own sandbox and reaches your data through **connectors**, so these versions:

- Read and write the recipe collection in the `elsoybean/meal-planning` GitHub repo **through the GitHub connector**, not the local filesystem.
- Use Claude's web search/fetch for research and source-checking.
- Write `.cook` files as text into the repo (no `cook` binary needed to author them).

## Setup

Add each `<name>/SKILL.md` here as a custom Skill in the consumer Claude app, with the GitHub connector enabled and able to reach `elsoybean/meal-planning`. Once added, they're usable from phone and laptop.

## What's here

- **kitchen-riff** — open-ended cooking collaboration when there's no fixed dish: ingredients on hand, a technique question, a flavor idea, "what goes with X." Source-grounded; hands off to a save skill when a riff becomes a keeper.
- **import-recipe**, **research-recipe**, **recipe-variant**, **quick-staple** — bring recipes into the collection, written to the repo via the connector (markdown + `.cook` where applicable).
- **build-profile**, **suggest-meal**, **meal-planner** — (coming next) profile and planning, reading/writing the repo via the connector.

## What's NOT here (stays Code / Pi-side)

- **add-to-shopping-list** and the CookCLI -> Bring feed: shopping runs on the Pi (`cook` shopping list + `tools/bring-sync`). A Desktop chat can't drive CookCLI or Bring — add recipes to the shopping list from the CookCLI web UI, and one-offs go straight into Bring.
- **recipe-card** PDF rendering: needs a local renderer. A Desktop chat can produce the HTML, but printing to PDF happens on a machine with a browser.
- `cook server`, `recipe-sync`: Pi-side, unchanged.

## Conventions (same as the Code skills)

Lead-noun-first naming ("Slaw, Sesame-Ginger" -> `slaw-sesame-ginger`); metric, grams by weight; four-column ingredient table (Quantity | Unit | Ingredient | Preparation); no anise/licorice. CookCLI config lives at `cook/config/aisle.conf` and `cook/config/pantry.conf`.
