# Desktop skills

Versions of the braizent skills adapted for the **consumer Claude apps** (web / desktop / mobile), as opposed to the Claude Code plugin in `../skills/`. These let you work with the recipe collection while chatting with Claude from your phone or laptop.

## How these differ from the Code skills

The Code skills assume a local checkout of the meal-planning repo, the `cook` binary on PATH, and local file tools (Read/Write/Grep). Claude Desktop runs in Claude's own sandbox and reaches your data through **connectors**, so these versions:

- Read and write the recipe collection in the `elsoybean/meal-planning` GitHub repo **through the GitHub connector**, not the local filesystem.
- Use Claude's web search/fetch for research and source-checking.
- Write `.cook` files as text into the repo (no `cook` binary needed to author them).

## Setup

Run `bash build.sh` to package the skills into `dist/<skill>.zip` (see Packaging below), then add each zip as a custom Skill in the consumer Claude app, with the GitHub connector enabled and able to reach `elsoybean/meal-planning`. Once added, they're usable from phone and laptop.

## Packaging (build.sh)

Consumer skills upload as self-contained folders, so each authoring skill references `_recipe-saver.md` as a **folder-local** file rather than a repo path. The canonical copy lives at `desktop-skills/_recipe-saver.md`; `build.sh` places a copy into each authoring skill at package time:

- `bash build.sh` (needs `zip`) stages each skill, drops the save contract into the authoring ones, and writes `dist/<skill>.zip`.
- The working skill folders stay clean (just `SKILL.md`); the bundled copies exist only in the build output.
- `dist/` is gitignored. Re-run after editing any skill or the contract.

(`build.sh` isn't marked executable as committed — run it with `bash build.sh`, or `chmod +x` it first.)

## What's here

- **kitchen-riff** — open-ended cooking collaboration when there's no fixed dish: ingredients on hand, a technique question, a flavor idea, "what goes with X." Source-grounded; can capture a riff that becomes a keeper.
- **import-recipe**, **research-recipe**, **recipe-variant**, **quick-staple** — bring recipes into the collection. Each does its own judgment, then hands a structured recipe to the save contract.
- **_recipe-saver.md** — the canonical, deterministic recipe-save contract: structured input -> slug, exact paths, `.md`/`.cook` rendering, never-overwrite, commit. The authoring skills delegate the mechanical save to it instead of re-deriving it each run. `build.sh` bundles a copy into each authoring skill's zip, referenced as a folder-local file (it isn't uploaded on its own).
- **build.sh**, **.gitignore** — packaging (above).
- **build-profile**, **suggest-meal**, **meal-planner** — (coming next) profile and planning, reading/writing the repo via the connector.

## What's NOT here (stays Code / Pi-side)

- **add-to-shopping-list** and the CookCLI -> Bring feed: shopping runs on the Pi (`cook` shopping list + `tools/bring-sync`). A Desktop chat can't drive CookCLI or Bring — add recipes to the shopping list from the CookCLI web UI, and one-offs go straight into Bring.
- **recipe-card** PDF rendering: needs a local renderer. A Desktop chat can produce the HTML, but printing to PDF happens on a machine with a browser.
- A true **sub-agent** for saving (cheap-model offload): that's a Claude Code feature — see `../agents/` when it's added. On Desktop the save runs in the same chat model, so the bundled contract buys consistency and no re-derivation rather than a cheaper model.
- `cook server`, `recipe-sync`: Pi-side, unchanged.

## Conventions (same as the Code skills)

Lead-noun-first naming ("Slaw, Sesame-Ginger" -> `slaw-sesame-ginger`); metric, grams by weight; four-column ingredient table (Quantity | Unit | Ingredient | Preparation); no anise/licorice. CookCLI config lives at `cook/config/aisle.conf` and `cook/config/pantry.conf`.
