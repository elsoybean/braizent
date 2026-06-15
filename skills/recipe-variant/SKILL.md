---
name: recipe-variant
description: Create a variant of an existing recipe (precise version, dietary adaptation, scaling, method change, etc.), then generate its Cooklang version.
---

# Recipe Variant

Create a modified version of an existing recipe — more precise, vegetarian, scaled, different method, whatever the user wants — saved alongside the original and made cookable.

## Input

The source recipe name and what they want to change. If either is unclear, ask; you can list `recipes/` if they're unsure which recipe.

## Work it out

Read the source recipe (`recipes/*/[slug].md`) and `PROFILE.md` if it helps (seasonings, household size, restrictions). Then work with the user on the actual changes. A few common shapes, for orientation rather than constraint:

- **Quick staple → precise**: pin down the to-taste amounts (ask what they actually use), expand the shorthand steps, and write it in the standard recipe format so it can be shared and carded.
- **Dietary / substitution**: swap ingredients and note any technique knock-ons.
- **Scaling**: handle what doesn't scale linearly — seasoning, leavening, timing, equipment.

## Conventions to apply

- **File** — same folder as the original, base slug plus an underscore suffix: `recipes/[slug]/[slug]_[suffix].md` (`_precise`, `_vegetarian`, `_double`, `_grilled`, …). Pick a short, obvious suffix.
- **Format** — standard recipe format (with the Quantity | Unit | Ingredient | Preparation table) when it's becoming precise or shareable; keep the quick-staple format only if it stays a loose personal memory aid.
- **Link** — in the variant's Personal Notes, link back to the original and say in one line what's different. Offer to add a reciprocal note on the original.

## Then generate the .cook

A variant is a distinct dish to cook, so run `to-cooklang` for it — producing `cook/[slug]_[suffix].cook`. (It skips the variant only if it's a quick staple with no precise measurements.)

## Finish

Link both files and summarize what changed.
