# Recipe-save contract

The dumb, deterministic half of recipe authoring: turn a finished, structured recipe into files at fixed paths in `elsoybean/meal-planning` (via the GitHub connector). No web, no research, no technique changes, no judgment. The calling skill already did all of that. A small model can run this. The only place that needs care is the `.cook` rendering.

The authoring skills (import-recipe, research-recipe, recipe-variant, quick-staple, and kitchen-riff's save off-ramp) all hand off here instead of re-deriving the mechanics.

## Input, provided by the calling skill; do not re-derive

A recipe object:

- `kind`: one of `standard` | `quick-staple` | `variant` | `reference-variant`
- `title`: comma-inverted, e.g. "Slaw, Sesame-Ginger"
- `base_slug` + `suffix`: required only when kind is `variant` or `reference-variant` (e.g. base_slug `karaage-miso`, suffix `vegetarian`)
- `servings` (int), `cuisine`, `course`, `time`, `source` { name, url }, `tags` (list), `description`
- `ingredients`: list of { quantity, unit, item, prep, section? } (section optional, groups rows under a heading)
- `steps`: ordered list of { text, cookware? (list), timer_min? }
- `notes?`, `development_notes?`, `research_sources?` (list of { title, url })

If a field required for the kind is missing, ask the calling skill. Never invent values, especially quantities.

## Step 1: slug

- `standard`, `quick-staple`: slug = title lowercased, every run of non-alphanumeric characters replaced with a single `-`, trimmed of leading/trailing `-`. "Chicken Thighs, Pan-Fried with Dirty Rice" -> `chicken-thighs-pan-fried-with-dirty-rice`
- `variant`, `reference-variant`: slug = `base_slug` + `_` + `suffix`.

## Step 2: target paths (exact)

- Markdown:
  - `standard`, `quick-staple`: `recipes/<slug>/<slug>.md`
  - `variant`, `reference-variant`: `recipes/<base_slug>/<slug>.md` (same folder as the original)
- Cooklang: `cook/<slug>.cook`, ONLY for kind `standard` and `variant`. NEVER write a `.cook` for `quick-staple` or `reference-variant`.

## Step 3: never overwrite

For each target path, check via the connector whether the file already exists. If it does, stop and report `already exists: <path>` back to the calling skill. Do not overwrite.

## Step 4: render the markdown

**Standard / variant:**

```
# <title>

<description>

**Servings:** <servings> · **Time:** <time> · **Cuisine:** <cuisine> · **Course:** <course>

## Ingredients

| Quantity | Unit | Ingredient | Preparation |
|---|---|---|---|
| <quantity> | <unit> | <item> | <prep> |
```

One row per ingredient. If sections are used, insert a row `| | | **<Section>** | |` before each group. For a **variant**, add under a `## Notes` section: `Variant of [<base title>](../<base_slug>/<base_slug>.md).` If `research_sources` is present, add a `## Research Sources` list of `- [<title>](<url>)`. End with `## Source` -> `[<source.name>](<source.url>)` (omit if no source). Omit any empty section.

**Quick-staple:**

```
# <title>

**Type:** Quick Staple

<description>

## Core Components
- <item>: <loose notes>      (no weighed amounts)

## Shopping Needs
- Usually buy: ...
- Always have: ...

## Preparation Notes
- <high-level memory joggers, not step-by-step>

## Variation Ideas
- ...

Tags: [quick-staple]
```

**Reference-variant:** use the standard layout, plus a one-line note on what this version teaches and where it's from.

## Step 5: render the .cook (standard / variant only)

```
---
title: <title>
servings: <servings>
cuisine: <cuisine>
course: <course>
time: <time>
source: <source.url>
tags: [<tags>]
---

== <Section> ==
<step text, with ingredients / cookware / timers marked inline>
```

`.cook` sections represent cooking phases (for example "Sauce", "Sear and Stir Fry", "Serve"), chosen to match how the dish is actually cooked. They do not need to mirror the ingredient list's sections one to one. Do not invent a standalone prep-only section (e.g. "Mise en Place") unless the calling skill's steps genuinely call for a distinct prep phase; normally, fold prep into the step where each ingredient is first used.

Marking, applied to each step's text:

- ingredient -> `@item{qty%unit}`; multiword item -> `@multi word item{qty%unit}`; no quantity -> `@item{}`
- cookware -> `#item{}`
- timer -> `~{<timer_min>%minutes}`
- to-taste / seasoning amounts -> lock with `=` so they don't scale, e.g. `@salt{=2%g}`

**Ingredient notes vs. steps.** Cooklang attaches a note to an ingredient with `{qty%unit}(note)`, no space between `}` and `(`. Use this for short, simple prep: dicing, mincing, slicing into strips, halving, coring, a couple words. For anything longer or more technique-heavy (a marinating time, a specific cut angle, a multi-clause instruction), describe it in the step text instead and leave the ingredient tag bare. The note is for shopping-list-level detail, not full instructions.

**No divided quantities.** Never write a single ingredient amount as "divided" or "half now, half later." Split it into two separate quantities, one per use, each with its own concrete amount (e.g. a `neutral oil{15%g}` reference at the sear step and a separate `neutral oil{15%g}` reference later), so the ingredient list totals correctly and each step is unambiguous on its own.

**No em dashes or double dashes.** Never use an em dash or `--` anywhere in a `.cook` file. Cooklang treats `--` as a line comment, so a double dash silently drops the rest of that line. Use a colon, a comma, a parenthetical, or a single hyphen with spaces around it instead. This also applies to the `.md` file and to any prose written back to the user during recipe work: no em dashes, and keep it concise rather than compensating with extra clauses.

Render straight from the structured ingredients and steps; don't re-interpret the recipe.

## Step 6: commit and report

Write the file(s) in one commit, message `Add <title>` (variants: `Add <title> (<suffix> variant)`), then report the exact paths written back to the calling skill.
