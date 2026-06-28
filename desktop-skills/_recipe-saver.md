# Recipe-save contract

The dumb, deterministic half of recipe authoring: turn a finished, structured recipe into files at fixed paths in `elsoybean/meal-planning` (via the GitHub connector). No web, no research, no technique changes, no judgment — the calling skill already did all of that. A small model can run this. The only place that needs care is the `.cook` rendering.

The authoring skills (import-recipe, research-recipe, recipe-variant, quick-staple, and kitchen-riff's save off-ramp) all hand off here instead of re-deriving the mechanics.

## Input — provided by the calling skill; do not re-derive

A recipe object:

- `kind`: one of `standard` | `quick-staple` | `variant` | `reference-variant`
- `title`: comma-inverted, e.g. "Slaw, Sesame-Ginger"
- `base_slug` + `suffix`: required only when kind is `variant` or `reference-variant` (e.g. base_slug `karaage-miso`, suffix `vegetarian`)
- `servings` (int), `cuisine`, `course`, `time`, `source` { name, url }, `tags` (list), `description`
- `ingredients`: list of { quantity, unit, item, prep, section? } — `section` optional, groups rows under a heading
- `steps`: ordered list of { text, cookware? (list), timer_min? }
- `notes?`, `development_notes?`, `research_sources?` (list of { title, url })

If a field required for the kind is missing, ask the calling skill — never invent values, especially quantities.

## Step 1 — slug

- `standard`, `quick-staple`: slug = title lowercased, every run of non-alphanumeric characters replaced with a single `-`, trimmed of leading/trailing `-`. "Chicken Thighs, Pan-Fried with Dirty Rice" -> `chicken-thighs-pan-fried-with-dirty-rice`
- `variant`, `reference-variant`: slug = `base_slug` + `_` + `suffix`.

## Step 2 — target paths (exact)

- Markdown:
  - `standard`, `quick-staple`: `recipes/<slug>/<slug>.md`
  - `variant`, `reference-variant`: `recipes/<base_slug>/<slug>.md` (same folder as the original)
- Cooklang: `cook/<slug>.cook` — ONLY for kind `standard` and `variant`. NEVER write a `.cook` for `quick-staple` or `reference-variant`.

## Step 3 — never overwrite

For each target path, check via the connector whether the file already exists. If it does, stop and report `already exists: <path>` back to the calling skill. Do not overwrite.

## Step 4 — render the markdown

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

One row per ingredient. If sections are used, insert a row `| | | **<Section>** | |` before each group. For a **variant**, add under a `## Notes` section: `Variant of [<base title>](../<base_slug>/<base_slug>.md).` If `research_sources` is present, add a `## Research Sources` list of `- <title> — <url>`. End with `## Source` -> `<source.name> — <source.url>` (omit if no source). Omit any empty section.

**Quick-staple:**

```
# <title>

**Type:** Quick Staple

<description>

## Core Components
- <item> — <loose notes>      (no weighed amounts)

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

## Step 5 — render the .cook (standard / variant only)

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

One `== Section ==` header per ingredient section, in order (omit if no sections). Marking, applied to each step's text:

- ingredient -> `@item{qty%unit}`; multiword item -> `@multi word item{qty%unit}`; no quantity -> `@item{}`
- cookware -> `#item{}`
- timer -> `~{<timer_min>%minutes}`
- to-taste / seasoning amounts -> lock with `=` so they don't scale, e.g. `@salt{=2%g}`

Render straight from the structured ingredients and steps; don't re-interpret the recipe.

## Step 6 — commit and report

Write the file(s) in one commit, message `Add <title>` (variants: `Add <title> (<suffix> variant)`), then report the exact paths written back to the calling skill.
