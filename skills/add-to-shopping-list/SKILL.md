---
name: add-to-shopping-list
description: Get a recipe's or meal's ingredients onto the shared shopping list via the CookCLI -> Bring flow.
---

# Add to Shopping List

Shopping runs through CookCLI and Bring now, so this skill no longer builds markdown lists or allocates quantities by hand. CookCLI aggregates and scales, `cook/config/pantry.conf` drops the staples, `cook/config/aisle.conf` routes each item to a store channel, and the Pi's `bring-sync` (in braizent `tools/`) pushes the result into the shared Bring! list — channel in each item's note. Bring is where the user and Jess check items off and add one-offs by voice.

## What "adding" means now

- **Recipes** -> put them on the CookCLI shopping list as references (`./[slug].cook`, plus a `{multiplier}` to scale). That list (`cook/.shopping-list`) is local server state on the kitchen Pi (gitignored, not a repo file), so it's managed through the running CookCLI server's UI or API, not by editing the repo. If you can't reach the server, identify the exact recipe refs to add and hand them to the user to add there.
- **One-off, non-recipe items** (the "we're out of dish soap" things) -> straight into Bring, including by voice. CookCLI can't hold ad-hoc items, so don't model them as fake recipes.

## Preview

`bring-sync.py --dry-run` on the Pi prints exactly what would land in Bring from the current CookCLI list — handy before a grocery run.
