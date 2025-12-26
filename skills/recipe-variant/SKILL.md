---
name: recipe-variant
description: Create a variant of an existing recipe with modifications for any purpose
---

# Recipe Variant Creator

This skill creates a variant of an existing recipe with modifications specified by the user. Variants can be created for any purpose: making measurements more precise, dietary adaptations, ingredient substitutions, scaling beyond simple multiplication, technique changes, or any other modification the user envisions.

## Step 1: Get the Source Recipe

The user must provide the name of the recipe they want to create a variant of. If no name is provided, ask for it before proceeding.

You can offer to list available recipes by searching the `./recipes/` directory if the user is unsure.

## Step 2: Find and Read the Source Recipe

Use the Glob tool to search for the recipe markdown file in `./recipes/`:
- Search for recipe folders: `recipes/*/[recipe-name].md`
- If the user provided an exact filename, use that
- Otherwise, search for files matching the recipe name pattern

If multiple matches are found, ask the user to clarify which recipe they want.
If no match is found, inform the user and offer to list available recipes.

Use the Read tool to load the complete source recipe markdown file.

## Step 3: Read User Profile (If Helpful)

Use the Read tool to load `./PROFILE.md` if it would help with the variant creation (e.g., understanding standard seasonings, household size, dietary restrictions).

## Step 4: Understand the Variant Purpose

Ask the user what changes they want to make to create this variant. Be open-ended and let them describe their intent.

**Ask:** "What kind of variant would you like to create from this recipe? For example:"
- Making measurements more precise for sharing with others
- Making it vegetarian/vegan
- Substituting ingredients (different protein, vegetables, etc.)
- Adapting for dietary restrictions (gluten-free, dairy-free, etc.)
- Scaling to a different size when simple multiplication won't work
- Changing the cooking method (oven to grill, stovetop to slow cooker, etc.)
- Any other modification you have in mind

Listen to their response and work with them to understand exactly what they want to change.

## Step 5: Determine the Variant Suffix

Work with the user to choose a short, descriptive suffix for the variant filename.

The suffix should:
- Start with an underscore
- Be lowercase
- Use hyphens for multi-word suffixes
- Clearly indicate what makes this variant different

**Common suffix examples:**
- `_precise` - Detailed measurements and instructions for sharing
- `_vegetarian` - Vegetarian adaptation
- `_gluten-free` - Gluten-free adaptation
- `_double` or `_scaled-12` - Larger batch
- `_grilled` - Different cooking method
- `_spicy` - Spice level variation
- `_simplified` - Easier/faster version
- `_instant-pot` - Different equipment

**Ask the user:** "What suffix would you like to use for this variant? This will be added to the filename like `[recipe-name]_[suffix].md`"

If the user is unsure, suggest one based on their stated purpose.

## Step 6: Gather Details for the Variant

Work with the user to make the specific changes to the recipe. The level of interaction depends on what they're changing:

### For Adding Precision (Quick Staple → Precise Recipe)

Go through each component:

**Ingredients:**
- Convert "to taste" or flexible amounts to specific quantities
- Ask user for typical amounts they use
- Confirm measurements for seasonings
- List out all ingredients explicitly

**Instructions:**
- Expand high-level steps into detailed numbered instructions
- Add temperatures, times, and visual cues
- Explain techniques the source recipe assumes you know

**Metadata:**
- Convert approximate times (~30 min) to specific times (30 minutes)
- Convert flexible servings to specific counts
- Add cuisine and category if missing

### For Dietary Adaptations

**Ask about:**
- Which ingredients need substitution
- What substitutes to use
- Any technique changes needed
- Any notes about how the adaptation affects the dish

### For Scaling

**Ask about:**
- Target serving size
- Any ingredients that don't scale linearly (seasonings, leavening, etc.)
- Equipment changes needed for larger/smaller batches
- Timing adjustments

### For Other Modifications

**Work with the user to:**
- Identify what changes from the original
- Document the new approach
- Note any important differences in technique or outcome

## Step 7: Determine Recipe Format

Based on the source recipe and variant purpose, use the appropriate format:

### Use Standard Recipe Format When:
- Adding precision to a quick staple recipe
- Creating a variant that will be shared with others unfamiliar with the dish
- The user wants detailed, step-by-step instructions

### Use Quick Staple Format When:
- Modifying an existing quick staple and keeping it flexible
- The variant is still a personal memory aid, not for sharing
- The user wants to preserve the flexible nature

### Use Source Format When:
- The source is a standard recipe and changes are minor
- Format doesn't need to change, just content

**Ask the user which format makes sense if it's not obvious.**

## Step 8: Create the Variant Recipe File

Use the Write tool to create the variant file at `./recipes/[recipe-folder]/[base-name]_[suffix].md`

### 8.1 Standard Recipe Format Template

```markdown
# [Recipe Title] ([Variant Description])

**Source:** Original recipe (variant)
**URL:** -
**Cuisine:** [Cuisine Type]
**Category:** [Category]
**Servings:** [Number]
**Total Time:** [Time]
**Active Time:** [Time]

## Description

[1-2 sentence description of the dish]

*This is a [variant type] variant of the original recipe. [Brief note about what's different]*

## Ingredients

| Quantity | Unit | Ingredient | Preparation |
|----------|------|------------|-------------|
| [qty]    | [unit] | [ingredient] | [prep] |

## Instructions

1. [Detailed step]
2. [Detailed step]
...

## Notes from Source

- [Any important notes from the original]

## Personal Notes

- Created from: [recipes/folder/original-recipe.md](original-recipe.md)
- [Specific notes about this variant]

## Tags

[original-tags] [variant] [variant-specific-tags]
```

### 8.2 Quick Staple Format Template

```markdown
# [Recipe Title] ([Variant Description])

**Type:** Quick Staple (Variant)
**Typical Meal Slot:** [Weeknight/Weekend/etc.]
**Total Time:** ~[X] minutes
**Servings:** Flexible - adjust as needed (typically [X])

## Description

[Overview and why this variant exists]

## Core Components

[Component descriptions with flexibility notes]

## Shopping Needs

[What to buy]

## Preparation Notes

[High-level steps]

## Variation Ideas

[Additional variations]

## Meal Planning Notes

[When to use this]

## Personal Notes

- Created from: [recipes/folder/original-recipe.md](original-recipe.md)
- [Why this variant was created]

## Tags

[quick-staple] [variant] [variant-specific-tags]
```

### 8.3 Important: Document the Relationship

Always include in Personal Notes:
- Link back to the original recipe
- Brief explanation of what makes this variant different
- Any context about why this variant was created

## Step 9: Confirm Completion

After successfully creating the variant file, inform the user:

"Successfully created the '[Variant Name]' variant of '[Recipe Name]'!

**Original recipe:** [recipes/folder-name/original-name.md](recipes/folder-name/original-name.md)
**New variant:** [recipes/folder-name/variant-name_suffix.md](recipes/folder-name/variant-name_suffix.md)

**What's different:**
[Bullet list of key changes]

**Format used:** [Standard Recipe / Quick Staple]

This variant lives in the same folder as the original recipe. Both versions are maintained independently, so you can:
- Edit either version without affecting the other
- Create recipe cards from either version
- Make additional variants if needed
- Use whichever version suits your current need"

## Step 10: Offer to Update Original Recipe

Ask the user if they'd like to add a note to the original recipe mentioning the variant exists:

"Would you like me to add a note to the original recipe indicating this variant is available?"

If yes, use the Edit tool to add a line in the Personal Notes section:
```markdown
- **[Variant type] variant available:** See [recipe-name_suffix.md](recipe-name_suffix.md) - [one-line description]
```

## Important Notes

**Flexibility is Key:**
- There's no limit to the types of variants users might want
- Don't constrain the user to predefined categories
- Work with them to understand and document whatever changes they want

**Maintain Relationships:**
- Always link back to the original recipe
- Consider bidirectional links (original → variant, variant → original)
- Keep variants in the same folder as the original

**Variant Naming:**
- Always use underscore prefix for variant suffix
- Keep the base filename identical to the original
- This makes it easy to identify related recipes in file listings

**Multiple Variants:**
- Users can create multiple variants of the same recipe
- Each variant is independent and serves a different purpose
- Examples: `recipe.md`, `recipe_precise.md`, `recipe_vegetarian.md`, `recipe_double.md`

**Recipe Card Integration:**
- The recipe-card skill will check for `_precise` variants specifically
- Users can make recipe cards from any variant, not just precise ones
- When the recipe-card skill finds a source that lacks precision, it will offer to create a `_precise` variant first

---

## Step 11: Complete

The recipe-variant skill is complete. The user now has a new variant of their recipe that serves their specific purpose.
