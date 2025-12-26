---
name: import-recipe
description: Imports a recipe from a URL to store it in a regular markdown file locally
---

# Recipe Import Workflow

## Step 1: Get the URL
The user must provide a recipe URL. If no URL is provided, ask for it before proceeding.

## Step 2: Fetch the Web Page
Use the WebFetch tool to retrieve the recipe page content. In your prompt, instruct it to extract:
- Recipe title
- Short description
- Source name
- Cuisine type
- Recipe category (e.g., soup, stew, main course, side dish, dessert, appetizer, salad, etc.)
- Servings count
- Total time
- Active/prep time (if available)
- Full ingredients list with quantities and units
- Step-by-step instructions
- Cooking temperatures (note if in Fahrenheit)
- Any special notes, tips, or variations mentioned

Look for structured data first (JSON-LD, schema.org Recipe metadata), then fall back to parsing the HTML content if structured data is not available.

## Step 3: Process and Standardize the Data

### 3.1 Title Formatting
Transform the title so the main food item comes first, with descriptors after a comma:
- "Classic Lasagna" → "Lasagna, Classic"
- "Creamy Leek and Potato Soup" → "Leek and Potato Soup, Creamy"
- "Easy Weeknight Chicken Stir Fry" → "Chicken Stir Fry, Easy Weeknight"
- "The Best Chocolate Cake" → "Chocolate Cake, The Best"

If the title is already in the correct format or is a simple name without adjectives (e.g., "Lasagna", "Minestrone"), leave it as is.

### 3.2 Measurements Conversion
- Convert all ingredient measurements to metric units:
  - Cups → ml (1 cup = 240ml)
  - Tablespoons (tbsp) → ml (1 tbsp = 15ml)
  - Teaspoons (tsp) → ml (1 tsp = 5ml)
  - Ounces (oz) → grams (1 oz = 28g)
  - Pounds (lb) → grams or kg (1 lb = 454g)
  - Fahrenheit → Celsius ((°F - 32) × 5/9 = °C)
- Keep common units like "cloves", "pieces", "whole", etc. as-is
- Round to sensible values (e.g., 237ml → 240ml)

### 3.3 Ingredient Table Structure
Parse each ingredient into four columns:
1. **Quantity**: The numeric amount (e.g., "2", "1/2", "240")
2. **Unit**: The measurement unit (e.g., "ml", "g", "cloves", "whole")
3. **Ingredient**: The main ingredient name (e.g., "onion", "flour", "olive oil")
4. **Preparation**: How to prepare it (e.g., "diced", "peeled and quartered", "sifted", "room temperature")

If an ingredient has no quantity (e.g., "Salt to taste"), use "-" for quantity and unit.
If no preparation is specified, leave that column empty.

### 3.4 Generate Tags
Create 5-10 relevant tags based on:
- Main ingredients (e.g., "chicken", "pasta", "tomato")
- Cuisine type (e.g., "italian", "thai", "mexican")
- Category (e.g., "soup", "dessert", "main-course")
- Cooking method (e.g., "baked", "grilled", "slow-cooker")
- Dietary attributes (e.g., "vegetarian", "gluten-free") if clearly applicable
- Time commitment (e.g., "quick", "weeknight", "make-ahead")

Format tags in lowercase with hyphens for multi-word tags.

## Step 4: Generate the Filename
1. Take the formatted recipe title
2. Convert to lowercase
3. Replace spaces with hyphens
4. Remove special characters (keep only letters, numbers, hyphens)
5. Examples:
   - "Lasagna, Classic" → "lasagna-classic.md"
   - "Leek and Potato Soup, Creamy" → "leek-and-potato-soup-creamy.md"
   - "Pad Thai" → "pad-thai.md"

## Step 5: Create the Recipe Folder and Markdown File

### 5.1 Create the Recipe Folder
Create a folder at `./recipes/[filename]/` using the Bash tool:
```bash
mkdir -p recipes/[filename]
```

### 5.2 Create the Markdown File
Use the Write tool to create a file at `./recipes/[filename]/[filename].md` with this exact structure:

```markdown
# [Recipe Title]

**Source:** [Source Name]
**URL:** [Source URL]
**Cuisine:** [Cuisine Type]
**Category:** [Category]
**Servings:** [Number]
**Total Time:** [Time]
**Active Time:** [Time] *(if available)*

## Description

[Short description of the recipe]

## Ingredients

| Quantity | Unit | Ingredient | Preparation |
|----------|------|------------|-------------|
| [qty]    | [unit] | [ingredient] | [prep] |
| [qty]    | [unit] | [ingredient] | [prep] |

## Instructions

1. [First step]
2. [Second step]
3. [Continue numbered steps...]

## Notes from Source

- [Important note or tip from the original recipe]
- [Another note if applicable]
- *(Leave this section empty if no notes from source)*

## Personal Notes

- *(Space for user to add their own notes)*

## Tags

[tag1] [tag2] [tag3] [tag4] [tag5]
```

## Step 6: Confirm Completion
After successfully creating the file, inform the user:
- The recipe title
- The folder and filename where it was saved
- A brief confirmation message

Example: "Successfully imported 'Lasagna, Classic' and saved to [recipes/lasagna-classic/lasagna-classic.md](recipes/lasagna-classic/lasagna-classic.md)"

The recipe now lives in its own folder where future assets (HTML card, PDF, images) can be stored alongside the markdown file.
