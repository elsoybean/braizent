# braizent

A Claude Code plugin of meal-planning and recipe skills. The **skills** live here; your **data** (recipes, meal plans, profile) lives in your own meal-planning project. This repo also carries the Raspberry Pi operational tooling in `tools/`.

## The two layers

Your meal-planning data has two layers:

- **Authoring layer** — `recipes/`, `meal-plans/`, `PROFILE.md`: human-readable markdown that you and these skills write and edit.
- **Cooking layer** — `cook/`: Cooklang `.cook` files plus `cook/config/aisle.conf` and `cook/config/pantry.conf`, served by [CookCLI](https://cooklang.org) (typically `cook server` on a Raspberry Pi) for browsing, scaling, timers, and shopping. Generated from the markdown by `to-cooklang`, but independently editable — the two are deliberately not auto-synced.

Recipe markdown is the authoring source of truth; `.cook` is authoritative for cooking.

## Conventions

- **Recipe naming** — lead with the dish, modifiers after a comma; the slug is that lowercased and hyphenated. "Slaw, Sesame-Ginger" -> `slaw-sesame-ginger`; "Chicken Leg Quarters, Roasted with Potatoes and Carrots" -> `chicken-leg-quarters-roasted-with-potatoes-and-carrots`. Each recipe lives in `recipes/[slug]/[slug].md`; variants are `[slug]_[suffix].md` in the same folder.
- **Measurements** — metric, grams by weight (the household cooks by scale).
- **Ingredient table** — standard recipes use a four-column table (Quantity | Unit | Ingredient | Preparation). This is the contract `to-cooklang` and `recipe-card` parse, so it stays consistent.

## Skills

Auto-discovered from `skills/` (see `.claude-plugin/plugin.json`).

**Recipe creation**
- **import-recipe** — fetch a recipe from a URL into `recipes/`, then generate its `.cook`.
- **research-recipe** — research a dish (simple / authentic / refined, culturally sensitive, sources credited), develop the user's version, save it plus reference variants, and generate the main recipe's `.cook`.
- **recipe-variant** — make a variant (precise, vegetarian, scaled, method change) alongside the original, with its own `.cook`.
- **quick-staple** — capture a flexible from-memory recipe with no precise amounts; excluded from `cook/` until a `_precise` variant makes it cookable.
- **to-cooklang** — convert recipe markdown to `cook/[slug].cook` (skips quick-staples, never overwrites).

**Planning & cooking**
- **meal-planner** — build a profile- and leftover-aware plan and feed the week's recipes into the shopping flow.
- **suggest-meal** — suggest a complete meal (main + sides) for a date, collection first then web.
- **recipe-card** — printable one-page card (HTML + PDF), primarily from `.cook`.
- **build-profile** — create or update `PROFILE.md`, and regenerate `cook/config/aisle.conf` and `pantry.conf` from it.
- **add-to-shopping-list** — put recipes on the CookCLI shopping list so the Bring feed has something to push.

## Shopping

Shopping runs through CookCLI and Bring!, not markdown lists:

- CookCLI generates the recipe-derived list — aggregated, scaled, `pantry.conf` staples removed, grouped by `aisle.conf` store channel (Knuspr / Rewe / Asian market / Hand-pick).
- `tools/bring-sync.py` (on the Pi) pushes that into a shared Bring! list, the store channel written into each item's note after the quantity.
- One-off and voice-added items live natively in Bring; CookCLI can't hold ad-hoc items, so they're not modeled as recipes.

## tools/ (Raspberry Pi)

Operational scripts that run on the kitchen Pi — not part of the plugin's skills, but version-controlled here since this is the code repo:

- **recipe-sync** — two-way git sync between the Pi's CookCLI web-UI edits and commits made elsewhere.
- **bring-sync.py** — the CookCLI -> Bring! feeder described above.

See `tools/README.md` for setup. Secrets (Bring login, GitHub deploy key) stay on the Pi and never enter the repo.

## Data layout (your project)

```
my-meals/
├── PROFILE.md
├── recipes/[slug]/[slug].md        # authoring layer (+ [slug]_[suffix].md variants, card .html/.pdf)
├── meal-plans/[range].md
└── cook/                            # cooking layer (CookCLI)
    ├── [slug].cook
    └── config/
        ├── aisle.conf               # store-channel routing (generated from PROFILE.md)
        └── pantry.conf              # always-on-hand staples (generated from PROFILE.md)
```

## Adding a skill

Add `skills/[name]/SKILL.md` with `name`/`description` frontmatter and concise, intent-focused instructions — describe the goal, constraints, and the shape of inputs and outputs, and trust the model to execute rather than scripting every step.

---

_Last updated: 2026-06-15_
