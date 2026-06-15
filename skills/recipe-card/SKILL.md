---
name: recipe-card
description: Make a printable one-page recipe card (HTML + PDF) from a recipe, primarily from its Cooklang .cook file.
---

# Recipe Card

Produce a clean, one-page printable card for a recipe and save it alongside the source.

## Source (prefer .cook)

Card from the recipe's `.cook` file when it has one — that's the cooking layer, and it covers `.cook`-only recipes too (e.g. a slaw built directly in `cook/`, with no markdown). Get structured data with `cook recipe -f json cook/[slug].cook` (CookCLI parses ingredients, cookware, timers, and metadata for you), or render via `cook report` with a template if you'd rather CookCLI do the layout.

Fall back to the markdown in `recipes/[slug]/` only when there's no `.cook` — typically a quick staple. A quick staple has no real measurements; if the user wants a shareable card, offer to make a `_precise` variant first (via `recipe-variant`), which also gives it a `.cook`. Otherwise card the loose version as-is.

## Card design

A single page, print-friendly: title and key metadata (servings, time, cuisine) up top, a compact two-column ingredient list, numbered steps, and source/notes in a footer. Serif headings, restrained color, tight margins so it fits on one page. Save the HTML next to the source.

## PDF

Render the HTML to PDF with whatever's on the machine — headless Chrome/Chromium, or `weasyprint`/`wkhtmltopdf`. If none is available, save the HTML and tell the user to print-to-PDF from the browser.

## Finish

Link the files you created.
