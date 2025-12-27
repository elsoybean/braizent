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

**COST OPTIMIZATION:** Steps 3.1, 3.2, and 3.3 are mechanical tasks perfect for fast agents. Consider spawning a task-optimized agent with the Task tool to handle:
- Title reformatting using the algorithm below
- Unit conversions using the lookup tables below
- Tag generation using the decision tree below

These straightforward operations cost ~70% less with a fast model compared to using a single capable model for everything.

### 3.1 Title Formatting

**Follow this algorithm exactly to reformat the title:**

#### Step 1: Identify Descriptors at the Start
Scan the beginning of the title for these common descriptor patterns:

**Adjectives (quality/style descriptors):**
- Classic, Creamy, Easy, Best, Perfect, Ultimate, Simple, Quick, Authentic, Traditional, Homemade, Grandma's, Mom's, Restaurant-Style, Homestyle, Old-Fashioned, Rustic, Elegant, Fancy, etc.

**Superlatives:**
- The Best, The Ultimate, The Perfect, The Easiest, The Most, etc.

**Time markers:**
- Quick, Easy, 30-Minute, Weeknight, Weekend, Make-Ahead, Slow-Cooker, Instant-Pot, etc.

**Quality markers:**
- Restaurant-Style, Homestyle, Grandma's, Mom's, Chef's, Authentic, Traditional, etc.

#### Step 2: Identify the Main Food Item
The main food item is usually:
- The first significant **noun** (or noun phrase) after removing descriptors
- OR the last significant noun before words like "Recipe" or "Dish"

**Examples:**
- "Classic **Lasagna**" → main item is "Lasagna"
- "Easy Weeknight **Chicken Stir Fry**" → main item is "Chicken Stir Fry"
- "The Best **Chocolate Cake**" → main item is "Chocolate Cake"
- "Creamy **Leek and Potato Soup**" → main item is "Leek and Potato Soup"

#### Step 3: Apply Transformation Rules

**Rule 1: If title starts with descriptor(s)** → Move descriptors after comma
- "Classic Lasagna" → "Lasagna, Classic"
- "The Best Chocolate Cake" → "Chocolate Cake, The Best"
- "Easy Weeknight Chicken Stir Fry" → "Chicken Stir Fry, Easy Weeknight"

**Rule 2: If title is simple (no leading descriptors)** → Keep as-is
- "Lasagna" → "Lasagna" (no change)
- "Minestrone" → "Minestrone" (no change)
- "Chicken Tikka Masala" → "Chicken Tikka Masala" (tikka is part of dish name, not a descriptor)

**Rule 3: If descriptors are in middle/end** → Keep as-is
- "Chicken Tikka Masala" → Keep (tikka is integral to the dish)
- "Pad Thai" → Keep (pad is part of dish name)
- "Beef Bourguignon" → Keep (bourguignon is integral)

#### Step 4: Validate Result
After transformation, check:
- Main food item is first ✓
- Comma properly separates main from descriptors ✓
- No double commas or trailing commas ✓
- Dish name makes sense ✓

#### Common Patterns
- "Adjective Food" → "Food, Adjective"
- "The Adjective Food" → "Food, The Adjective"
- "Adjective1 Adjective2 Food" → "Food, Adjective1 Adjective2"
- "Food" → "Food" (no change)
- "Food with Ingredient" → "Food with Ingredient" (no change)

### 3.2 Measurements Conversion

**IMPORTANT: Use this exact conversion table. Do NOT estimate or approximate - look up the conversion below.**

#### Volume Conversions (Use These Exact Values)
- 1 cup = 240ml
- 3/4 cup = 180ml
- 2/3 cup = 160ml
- 1/2 cup = 120ml
- 1/3 cup = 80ml
- 1/4 cup = 60ml
- 1 tablespoon (tbsp, T) = 15ml
- 1 teaspoon (tsp, t) = 5ml
- 1 fluid ounce (fl oz) = 30ml
- 1 pint (US) = 475ml
- 1 quart (US) = 950ml
- 1 gallon (US) = 3.8L

**For combinations** (e.g., 2 1/4 cups):
1. Convert whole number: 2 cups = 480ml
2. Convert fraction: 1/4 cup = 60ml
3. Add: 480ml + 60ml = 540ml

#### Weight Conversions (Use These Exact Values)
- 1 ounce (oz) = 28g
- 2 oz = 56g
- 4 oz = 113g
- 8 oz = 227g
- 1 pound (lb) = 454g
- 2 lb = 908g (can round to 900g)
- Note: 16 oz = 1 lb = 454g

#### Temperature Conversions
**Use this formula**: (°F - 32) × 5/9 = °C

**Common baking temperatures** (use these exact values):
- 300°F = 150°C
- 325°F = 165°C
- 350°F = 175°C
- 375°F = 190°C
- 400°F = 200°C
- 425°F = 220°C
- 450°F = 230°C
- 475°F = 245°C

**For other temperatures**, apply the formula then round to nearest 5°C.

#### Rounding Rules (Apply After Conversion)
- Volumes under 100ml: Round to nearest 5ml (e.g., 237ml → 240ml)
- Volumes 100-500ml: Round to nearest 10ml (e.g., 473ml → 475ml)
- Volumes over 500ml: Round to nearest 50ml (e.g., 847ml → 850ml)
- Weights under 100g: Round to nearest 5g (e.g., 84g → 85g)
- Weights 100-500g: Round to nearest 10g (e.g., 467g → 470g)
- Weights over 500g: Round to nearest 50g (e.g., 908g → 900g)

#### Keep As-Is (No Conversion Needed)
- cloves (garlic, etc.)
- pieces
- whole
- large/medium/small (descriptive sizes)
- "to taste"
- pinch
- bunch (for herbs)
- head (for cabbage, lettuce, garlic)

### 3.3 Ingredient Table Structure
Parse each ingredient into four columns:
1. **Quantity**: The numeric amount (e.g., "2", "1/2", "240")
2. **Unit**: The measurement unit (e.g., "ml", "g", "cloves", "whole")
3. **Ingredient**: The main ingredient name (e.g., "onion", "flour", "olive oil")
4. **Preparation**: How to prepare it (e.g., "diced", "peeled and quartered", "sifted", "room temperature")

If an ingredient has no quantity (e.g., "Salt to taste"), use "-" for quantity and unit.
If no preparation is specified, leave that column empty.

### 3.4 Generate Tags

**Follow this exact tag generation system to select 5-10 tags:**

#### ALWAYS Include These Tags (Mandatory)

**1. Timing Tag** (choose one):
- [under-15-min] if total time < 15 min
- [under-30-min] if total time < 30 min
- [under-60-min] if total time < 60 min
- [1-2-hours] if total time 60-120 min
- [long-cook] if total time > 120 min

**2. Meal Slot Tag** (choose all that apply):
- [weeknight] if under 60 min active time
- [weekend] if over 90 min total time OR complex technique
- [featured-dish] if > 2 hours OR special occasion appropriate

#### Protein Tags (choose one primary)
[chicken] [pork] [beef] [lamb] [fish] [seafood] [vegetarian] [vegan]

#### Cuisine Tags (choose one primary)
[italian] [french] [german] [chinese] [thai] [vietnamese] [mexican] [indian] [japanese] [korean] [mediterranean] [american] [polish] [british] [spanish] [middle-eastern] [greek]

#### Category Tags (choose one primary)
[soup] [stew] [salad] [pasta] [rice-dish] [noodles] [curry] [stir-fry] [roast] [casserole] [sandwich] [appetizer] [side-dish] [dessert] [breakfast] [brunch]

#### Cooking Method Tags (choose all that apply, max 2)
[baked] [roasted] [grilled] [pan-fried] [deep-fried] [steamed] [boiled] [braised] [slow-cooker] [pressure-cooker] [instant-pot] [air-fryer] [stovetop] [no-cook]

#### Optional Characteristic Tags (choose 1-3 if applicable)
[comfort-food] [crowd-pleaser] [make-ahead] [meal-prep] [one-pot] [sheet-pan] [freezer-friendly] [leftovers-friendly] [budget-friendly] [fancy] [date-night] [kid-friendly]

#### Dietary Tags (only if explicitly clear from recipe)
[gluten-free] [dairy-free] [nut-free] [low-carb] [high-protein] [keto] [paleo]

#### Ingredient-Based Tags (add 1-2 key ingredients if relevant)
[tomato] [garlic] [onion] [mushroom] [potato] [rice] [pasta] [cheese] [lemon] [ginger] [coconut] [chocolate] [etc.]

#### Final Tag Count
- **Minimum**: 5 tags (timing + meal slot + protein + cuisine + category)
- **Maximum**: 10 tags (add method + characteristics + ingredients)

**Format**: All tags lowercase with hyphens for multi-word tags (e.g., [slow-cooker], [comfort-food])

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
