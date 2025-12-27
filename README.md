# Meal Planner Skills Plugin

A Claude Code plugin providing intelligent meal planning skills. This plugin contains reusable skills that work with your meal planning data to help you create personalized meal plans, import recipes, generate shopping lists, and minimize food waste.

**Note:** This is a **plugin repository** containing the skills. Your actual meal planning data (recipes, meal plans, profile) lives in **your own project** using the structure documented below.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Skills](#skills)
- [User Profile System](#user-profile-system)
- [File Structure & Formats](#file-structure--formats)
- [Getting Started](#getting-started)
- [Workflow Examples](#workflow-examples)
- [Advanced Features](#advanced-features)

## Overview

This plugin provides meal planning skills built on the **Agent Skills Open Standard**, making them modular, extensible, and compatible with AI coding agents like Claude Code. These skills help you:

- **Plan meals** that match your tastes, dietary needs, and household size
- **Import recipes** from any URL with automatic parsing and standardization
- **Generate shopping lists** organized by store, section, and shopping day
- **Track inventory** of pantry staples and leftover ingredients
- **Minimize waste** by prioritizing ingredients that need to be used up
- **Learn over time** by capturing feedback on recipes and refining recommendations
- **Optimize shopping** around your schedule and preferred stores
- **Support health goals** without giving medical advice

### Key Principles

1. **User-centered**: Every recommendation respects your stated preferences, restrictions, and goals
2. **Iterative**: The system learns from feedback and improves over time
3. **Flexible**: Supports various planning styles (weekly, monthly, ad-hoc, recipe-centered)
4. **Practical**: Accounts for real-world constraints like shopping schedules, pantry inventory, and food waste
5. **Transparent**: All data is stored in human-readable markdown files that you can edit manually

## Features

### Core Features

- **Recipe Management**
  - Import recipes from any URL with automatic parsing
  - Standardized recipe format with metric measurements
  - Structured ingredient tables with quantity, unit, ingredient, and preparation columns
  - Tagging system for easy searching and filtering
  - Personal notes section for customizations and feedback

- **Intelligent Meal Planning**
  - Generate meal plans for any time period (days, weeks, months)
  - Consider serving sizes with appetite adjustments
  - Respect dietary restrictions and preferences absolutely
  - Balance variety, nutrition, and user taste preferences
  - Suggest meals based on ingredients that need to be used up
  - Build plans around specific recipes the user wants to try

- **Smart Shopping Lists**
  - Organized by store (Costco, Publix, corner store, etc.)
  - Grouped by section (produce, dairy, meat, pantry, etc.)
  - Separated by shopping day for multi-trip plans
  - Excludes pantry staples the user keeps in stock
  - Interactive checklist format for easy shopping
  - Quantity consolidation across multiple recipes

- **Inventory & Waste Tracking**
  - Track pantry staples and common ingredients
  - Record leftover ingredients from completed meal plans
  - Prioritize using up perishables in future plans
  - Minimize food waste through intelligent planning

- **Learning & Feedback**
  - Capture post-plan feedback on recipes
  - Record which meals were successful or need adjustments
  - Note which recipes to repeat or avoid
  - Track ingredient preferences discovered during cooking
  - Continuously refine the user profile

### Advanced Features

- **Multi-Store Optimization**: Plan shopping trips around bulk purchases, weekly runs, and daily pickups
- **Seasonal Awareness**: Consider seasonal ingredients and availability
- **Meal Prep Support**: Identify recipes suitable for batch cooking and meal prep
- **Leftover Integration**: Plan meals that complement each other and use leftovers
- **Budget Consciousness**: Track approximate costs and suggest budget-friendly alternatives
- **Nutritional Balance**: Support health goals like protein targets, calorie ranges, or macro ratios
- **Substitution Suggestions**: Recommend ingredient swaps based on allergies, preferences, or availability
- **Time Management**: Consider active vs. passive cooking time for weeknight vs. weekend meals

## Skills

This plugin provides modular skills following the **Agent Skills Open Standard**. Each skill is self-contained, documented in `SKILL.md` format, and can be invoked independently or as part of larger workflows. These skills work with your meal planning data in your own project.

### Implemented Skills

#### `import-recipe`
**Purpose**: Import a recipe from a URL and save it as a standardized markdown file locally.

**Capabilities**:
- Fetches recipe content from any URL
- Extracts structured data (JSON-LD, schema.org) or parses HTML
- Converts measurements to metric units
- Standardizes title format (main ingredient first)
- Generates structured ingredient tables
- Creates relevant tags
- Saves to `./recipes/` with consistent naming

**Location**: `skills/import-recipe/` (in this plugin)

#### `quick-staple`
**Purpose**: Capture a familiar staple recipe that you make regularly with minimal planning.

**Capabilities**:
- Quick interview process (less than 5 minutes)
- Captures high-level steps as memory aids
- Documents flexibility and variations
- Profile-aware: uses standard seasonings and shopping patterns
- Creates recipes tagged as `[quick-staple]` for easy identification

**Location**: `skills/quick-staple/` (in this plugin)

#### `recipe-variant`
**Purpose**: Create a variant of an existing recipe with modifications for any purpose.

**Capabilities**:
- General-purpose variant creation (precise measurements, dietary adaptations, scaling, cooking method changes, etc.)
- User-defined variant suffixes (e.g., `_precise`, `_vegetarian`, `_gluten-free`, `_double`)
- Flexible output formats (standard recipe or quick staple)
- Maintains relationship links between original and variant
- Supports multiple variants of the same recipe

**Location**: `skills/recipe-variant/` (in this plugin)

#### `recipe-card`
**Purpose**: Generate a printable recipe card PDF from a recipe in the collection.

**Capabilities**:
- Finds recipes by name in the collection
- Checks for `_precise` variants and offers to use them or create them
- Creates beautifully formatted HTML for printing with two-column ingredient layout
- Automatically generates PDF using Chrome headless mode (if Chrome is installed)
- Falls back to weasyprint or wkhtmltopdf if available
- Falls back to browser-based PDF generation instructions if no tools available
- Optimized layout for standard letter-size paper with 0.2-inch margins
- Includes all recipe sections (ingredients, instructions, notes)
- Adapts formatting for both precise and flexible recipes
- Clean, professional design suitable for kitchen use or sharing

**Location**: `skills/recipe-card/` (in this plugin)

#### `build-profile`
**Purpose**: Interview the user to create or update their profile with preferences and constraints.

**Capabilities**:
- Guided questionnaire covering 8 profile dimensions (household, preferences, restrictions, shopping, pantry, cooking style, health, budget)
- Two modes: create new profile or update existing profile
- Section-by-section or full profile updates
- Critical emphasis on dietary restrictions for safety
- Saves responses to `PROFILE.md` with proper structure and formatting
- Updates timestamp when modified

**Location**: `skills/build-profile/` (in this plugin)

#### `research-recipe`
**Purpose**: Research and develop a personalized version of any recipe from multiple sources with professional-level analysis.

**Capabilities**:
- Multi-perspective research: searches for simple, authentic, and refined versions of any dish
- Cultural sensitivity: prioritizes voices from the culture, especially first-generation immigrants
- Comprehensive analysis: compares techniques, ingredients, and approaches across versions
- Personalized development: tailors the recipe to user's preferences, equipment, and skill level
- Variant preservation: saves all research versions (simple, authentic, refined) for reference
- Proper attribution: preserves source URLs and credits for all recipe creators
- Profile-aware: adapts to household size, dietary restrictions, shopping patterns, and equipment

**How it works**:
1. User provides dish name
2. Conducts thorough web research for multiple versions
3. Presents comprehensive findings with cultural context
4. Collaborates with user to develop their perfect version
5. Saves personalized recipe plus research variants

**Location**: `skills/research-recipe/` (in this plugin)

#### `suggest-meal`
**Purpose**: Suggest a meal for a specific date with recipe discovery and side dish pairing.

**Capabilities**:
- Uses Bash date commands to verify dates (no LLM date arithmetic)
- Checks existing meal plans and offers to use or swap meals
- Gathers full meal context (people, time, ingredients, schedule)
- Searches recipe collection for matching options
- Falls back to web search if no good collection matches
- Presents 3-4 recipe options with reasoning
- Suggests appropriate side dishes (prefers simple descriptions over full recipes)
- Gets user approval before adding to meal plan
- Provides complete ingredient list for shopping integration
- Integrates with: import-recipe, quick-staple, meal-planner, research-recipe

**How it works**:
1. Verifies the target date using system tools
2. Checks if meal already planned for that date
3. Gathers context about the meal (people, time, constraints)
4. Searches recipes or web for appropriate options
5. Presents options and gets user approval
6. Suggests balanced side dishes
7. Optionally adds to meal plan
8. Returns complete ingredient list

**Location**: `skills/suggest-meal/` (in this plugin)

#### `quick-meal-pick`
**Purpose**: Fast, cost-optimized meal suggestion from local recipes (streamlined alternative to suggest-meal).

**Capabilities**:
- Quick tag-based search of local recipe collection
- Standard side dish pairing using template rules
- Minimal questions for fast decisions
- Uses fast models for 85-90% cost savings vs. suggest-meal
- Best for routine meals where any appropriate recipe works

**How it works**:
1. Gathers basic criteria (time, cuisine, protein) in single question batch
2. Searches local recipes by tags (mechanical search)
3. Applies standard side dish pairing rules by cuisine
4. Presents suggestion with option to add to shopping list
5. Falls back to full suggest-meal if no local matches

**Cost comparison**:
- quick-meal-pick: ~$0.10-0.15 (fast model, tag search)
- suggest-meal: ~$0.80-1.00 (capable model, context-aware reasoning)

**When to use**:
- ✅ Routine weeknight meals
- ✅ Quick decision needed
- ✅ Trust your recipe collection
- ❌ Special occasions (use suggest-meal)
- ❌ Need web search (use suggest-meal)
- ❌ Want creative suggestions (use suggest-meal)

**Location**: `skills/quick-meal-pick/` (in this plugin)

#### `add-to-shopping-list`
**Purpose**: Add ingredients for a specific meal to the appropriate shopping list with smart quantity tracking.

**Capabilities**:
- Reads profile to understand shopping patterns and pantry staples
- Filters out items always on hand vs. must purchase
- Determines appropriate shopping trip based on meal date and user's schedule
- Checks existing shopping lists for that trip
- Smart allocation: claims from existing purchases when possible to avoid over-purchasing
- Tracks quantities purchased vs. quantities claimed by meals
- Organizes by store and department (Produce, Meat & Seafood, Dairy & Eggs, etc.)
- Uses markdown checklists for easy marking off while shopping
- Handles multi-store shopping trips
- Realistic package sizes (can't buy 50g flour, must buy 1kg bag)
- Confirms pantry staple assumptions with user

**How it works**:
1. Reads profile for shopping context
2. Gets meal information and ingredients
3. Filters out pantry staples (with confirmation)
4. Determines which shopping trip should include these ingredients
5. Checks existing shopping lists
6. Smart allocation: claims from existing items or adds new items
7. Updates shopping list files (creates if needed)
8. Confirms pantry assumptions with user

**Location**: `skills/add-to-shopping-list/` (in this plugin)

#### `meal-planner`
**Purpose**: Create personalized meal plans with intelligent recipe selection and shopping lists. The central orchestrator skill.

**Capabilities**:
- Gathers planning goals and constraints for any time period
- Uses Bash date commands to verify all dates
- Reads profile for comprehensive context
- Checks recent meal plans to avoid repetition
- Builds detailed requirements for each meal
- **Orchestrates suggest-meal skill** for each meal with rich context
- Gets user approval for each meal before adding to plan
- **Orchestrates add-to-shopping-list skill** to add ingredients incrementally
- Tracks ingredient usage across meals for efficiency
- Generates complete meal plan file with schedule, shopping lists, and prep notes
- Presents consolidated shopping lists at the end
- Provides comprehensive summary with next steps

**How it works**:
1. Reads profile for context
2. Verifies dates using system tools
3. Gathers planning goals and constraints
4. Checks recent meal plans
5. Builds requirements for each meal
6. For each meal (in chronological order):
  - Invokes suggest-meal with detailed context
  - User approves the meal
  - Invokes add-to-shopping-list silently
  - Updates tracking for remaining meals
7. Generates meal plan file
8. Presents consolidated shopping lists
9. Provides final summary

**Integrates with:** suggest-meal (for each meal), add-to-shopping-list (after each approval)

**Location**: `skills/meal-planner/` (in this plugin)

### Skill Relationships

The skills work together in a coordinated workflow:

```
meal-planner (orchestrator)
├── suggest-meal (for each meal)
│   ├── Grep (search recipes)
│   ├── WebSearch (if no collection match)
│   ├── import-recipe (if user wants to save web recipe)
│   ├── quick-staple (if user wants to document known recipe)
│   └── research-recipe (if user wants thorough research)
└── add-to-shopping-list (after each approved meal)
    ├── Reads shopping lists
    ├── Smart allocation
    └── Updates shopping lists
```

Individual skills can also be used standalone:
- Use **suggest-meal** to plan a single meal without a full meal plan
- Use **add-to-shopping-list** to add ingredients for any recipe to your shopping
- Use **import-recipe**, **quick-staple**, or **research-recipe** to add recipes anytime

### Planned Skills

#### `capture-feedback`
**Purpose**: Capture feedback after completing a meal or meal plan.

**Capabilities**:
- Aggregate ingredients across all recipes
- Convert and consolidate quantities
- Organize by store and section
- Separate by shopping day
- Exclude pantry staples
- Format as interactive checklist
- Note which items are for which recipes

#### `capture-feedback`
**Purpose**: Collect feedback after completing a meal plan to improve future recommendations.

**Capabilities**:
- Review each recipe in the completed plan
- Capture success ratings and specific feedback
- Identify recipes to repeat or avoid
- Record leftover ingredients and quantities
- Update user profile with new preferences
- Suggest profile adjustments based on feedback

#### `search-recipes`
**Purpose**: Search the local recipe collection by ingredients, tags, cuisine, or other criteria.

**Capabilities**:
- Full-text search across recipe content
- Filter by tags, cuisine, category
- Search by ingredient (has/doesn't have)
- Sort by prep time, total time, servings
- Consider dietary restrictions
- Suggest recipes based on available ingredients

#### `adjust-servings`
**Purpose**: Scale recipe quantities to match the desired number of servings.

**Capabilities**:
- Recalculate all ingredient quantities
- Handle fractional conversions intelligently
- Consider appetite adjustments from profile
- Update recipe with new serving size

#### `suggest-substitutions`
**Purpose**: Recommend ingredient substitutions based on dietary needs, preferences, or availability.

**Capabilities**:
- Find allergen-free alternatives
- Suggest pantry swaps for missing ingredients
- Recommend based on user preferences
- Provide conversion ratios and usage notes

#### `analyze-nutrition`
**Purpose**: Estimate nutritional content of recipes and meal plans to support health goals.

**Capabilities**:
- Calculate approximate macros and calories
- Identify meals meeting specific nutritional targets
- Balance meal plans for nutritional variety
- Track progress toward dietary goals
- **Note**: Never provides medical advice

#### `export-meal-plan`
**Purpose**: Export meal plans and shopping lists to various formats for easy sharing and printing.

**Capabilities**:
- Export to PDF, CSV, plain text
- Generate printable shopping lists
- Create calendar-compatible formats (iCal)
- Share meal plans via email or messaging

## User Profile System

The user profile is the foundation of personalized meal planning. It's stored in `PROFILE.md` and should be both machine-readable and user-editable. Every skill begins by reading the profile to understand current preferences.

### Profile Dimensions

#### 1. Number of Servings

**What we capture**:
- Default household size (number of people)
- Variance by day of week (e.g., 2 on weekdays, 4 on weekends)
- Appetite adjustments (larger/smaller than typical recipe servings)
- Age ranges (kids, adults, teens) to estimate appropriate portions
- Whether user wants leftovers for lunch

**Why it matters**: Ensures meal plans produce the right amount of food without waste or shortages.

**Example**:
```markdown
## Servings
- Default: 2 adults
- Weekends: +2 kids
- Appetite: Slightly larger than average (multiply recipe servings by 1.2)
- Prefer: Some leftovers for next-day lunch
```

#### 2. Taste Preferences

**What we capture**:
- Favorite cuisines (Italian, Thai, Mexican, etc.)
- Preferred meal types (comfort food, light and fresh, adventurous)
- Flavor profiles (spicy, savory, sweet, umami)
- Ingredients they love and hate
- Frequency of variety (likes routine vs. needs diversity)
- Willingness to try new recipes

**Why it matters**: Meal plans only work if the user is excited to cook and eat the meals.

**Example**:
```markdown
## Taste Preferences
- Favorite cuisines: Italian, Japanese, Mediterranean
- Loves: Garlic, fresh herbs, seafood, roasted vegetables
- Dislikes: Cilantro, black licorice flavors, overly sweet sauces
- Spice tolerance: Medium (enjoys heat but not extreme)
- Variety: Prefers 5-6 different dinners per week, OK with repeating favorites
- Adventurousness: Willing to try new recipes 1-2x per month
```

#### 3. Dietary Restrictions

**What we capture**:
- Allergies (life-threatening or severe reactions)
- Intolerances (digestive issues, sensitivities)
- Religious restrictions (kosher, halal, etc.)
- Ethical choices (vegetarian, vegan, pescatarian)
- Avoided ingredients (personal preferences vs. restrictions)
- Cross-contamination concerns

**Why it matters**: This is **critically important**. We must **never** recommend meals that violate restrictions.

**Rules**:
- Always respect restrictions absolutely
- Flag any uncertainty about ingredients
- Better to exclude a questionable recipe than risk it
- Never suggest "you could just pick out the X"
- Support user's choices without judgment

**Example**:
```markdown
## Dietary Restrictions
- **SEVERE ALLERGY**: Tree nuts (anaphylaxis risk)
- **ALLERGY**: Shellfish (hives, swelling)
- Lactose intolerant (can tolerate hard cheeses, avoid milk/cream)
- Avoids: Red meat (ethical reasons), cilantro (taste)
- Cross-contamination: Exercise caution with tree nuts in shared facilities
```

#### 4. Shopping Schedule

**What we capture**:
- Preferred stores and shopping frequency
- Bulk shopping locations (Costco, Sam's Club)
- Regular grocery stores (Publix, Kroger, Whole Foods)
- Specialty stores (Asian market, farmer's market)
- Convenience stores for last-minute items
- Willingness to make multiple trips per week
- Online ordering vs. in-person preferences
- Typical shopping days

**Why it matters**: Optimizes meal planning around realistic shopping patterns and helps organize shopping lists effectively.

**Example**:
```markdown
## Shopping Schedule
- **Primary store**: Publix (Saturdays, weekly)
- **Bulk shopping**: Costco (once per month, first Saturday)
- **Specialty**: Asian market (every 2-3 weeks, flexible)
- **Backup**: Corner store (willing to go for 1-2 forgotten items)
- **Online**: Occasionally for heavy items or when sick
- Prefer: Single weekly trip, avoid daily shopping
```

#### 5. Pantry Staples

**What we track**:
- Ingredients always kept in stock
- Items that don't need to be on shopping lists
- Preferred brands or quality levels
- Quantities typically on hand
- Spice collection and dried herbs
- Oils, vinegars, and condiments
- Baking essentials

**Why it matters**: Prevents shopping lists from including obvious items and helps with recipe selection.

**Example**:
```markdown
## Pantry Staples (always in stock)
### Basics
- Salt (kosher, sea salt)
- Black pepper, red pepper flakes
- Olive oil, vegetable oil, sesame oil
- All-purpose flour, bread flour
- Sugar (white, brown)
- Baking powder, baking soda

### Spices & Herbs
- Garlic powder, onion powder, paprika, cumin, oregano, basil, thyme, cinnamon

### Condiments & Sauces
- Soy sauce, fish sauce, rice vinegar
- Dijon mustard, hot sauce
- Chicken/vegetable stock (boxed)

### Grains & Legumes
- Rice (white, brown, jasmine)
- Pasta (variety of shapes)
- Dried lentils, canned beans
```

#### 6. Health Goals

**What we capture**:
- Stated dietary goals (weight management, muscle building, general health)
- Nutritional targets (protein, fiber, calorie ranges)
- Meal timing preferences (intermittent fasting, etc.)
- Energy level considerations
- Specific nutrients of interest
- Concerns about blood sugar, cholesterol, etc.

**Critical rules**:
- **NEVER give medical advice**
- **NEVER insinuate we know what's best for their health**
- Support stated goals without endorsement
- Encourage consulting healthcare providers
- Provide information, not prescriptions

**Why it matters**: Many users have health goals we can support through meal selection while staying within appropriate boundaries.

**Example**:
```markdown
## Health Goals
*Note: This information supports your stated goals. Consult healthcare providers for medical advice.*

- Goal: Increase protein intake (target ~30g per dinner)
- Goal: Eat more vegetables (aim for 2-3 servings per dinner)
- Preference: Lower sodium when possible (not medically required)
- Interest: Mediterranean diet patterns
- Energy: Prefers lighter lunches, larger dinners
```

#### 7. Cooking Style & Constraints

**What we capture**:
- Skill level (beginner, intermediate, advanced)
- Available time on weekdays vs. weekends
- Kitchen equipment (slow cooker, instant pot, air fryer, etc.)
- Willingness to do meal prep
- Preference for quick vs. elaborate cooking
- Whether they enjoy cooking or see it as a chore

**Why it matters**: Ensures meal plans are realistic and enjoyable to execute.

**Example**:
```markdown
## Cooking Style
- Skill level: Intermediate (comfortable with most techniques)
- Weekday time: 30-45 minutes max active cooking
- Weekend time: Up to 2 hours for special recipes
- Equipment: Instant Pot, slow cooker, standard kitchen
- Meal prep: Willing to prep on Sundays for the week
- Attitude: Enjoys cooking but values efficiency
```

#### 8. Budget Considerations

**What we capture**:
- Weekly/monthly food budget
- Splurge ingredients vs. everyday staples
- Preference for budget-friendly recipes
- Bulk buying strategies
- Seasonal shopping preferences
- Store brand vs. name brand preferences

**Why it matters**: Keeps meal planning financially sustainable.

**Example**:
```markdown
## Budget
- Weekly grocery budget: ~$150-200 for 2 adults
- Comfortable with: Occasional expensive ingredients ($15-25) for special recipes
- Prefer: Budget-friendly weeknight meals, splurge on weekends
- Strategy: Buy proteins on sale, use seasonal produce
- Flexible: Will adjust budget for special occasions
```

### Profile File Format

The profile should be stored as `PROFILE.md` in the root directory with the following structure:

```markdown
# User Profile

*Last updated: YYYY-MM-DD*

## Household & Servings
[Content as described above]

## Taste Preferences
[Content as described above]

## Dietary Restrictions
[Content as described above]

## Shopping Schedule
[Content as described above]

## Pantry Staples
[Content as described above]

## Health Goals
[Content as described above]

## Cooking Style & Constraints
[Content as described above]

## Budget Considerations
[Content as described above]

## Learning Notes
*This section is automatically updated based on feedback*

### Recipes to Repeat
- [Recipe name]: [Why it was great]

### Recipes to Avoid
- [Recipe name]: [What didn't work]

### Discovered Preferences
- [Date]: [Insight from feedback]
```

## File Structure & Formats

### Plugin Structure (This Repository)

This plugin repository contains the skills:

```
braizent/ (plugin repository)
├── README.md                          # This file - plugin documentation
├── CLAUDE.md                          # Instructions for Claude
└── skills/                            # Agent skills directory
    ├── import-recipe/
    │   └── SKILL.md                  # Recipe import skill
    ├── quick-staple/
    │   └── SKILL.md                  # Quick staple recipe skill
    ├── recipe-variant/
    │   └── SKILL.md                  # Recipe variant creator skill
    ├── recipe-card/
    │   └── SKILL.md                  # Recipe card generator skill
    ├── build-profile/
    │   └── SKILL.md                  # Profile builder skill
    ├── research-recipe/
    │   └── SKILL.md                  # Recipe research & development skill
    ├── suggest-meal/
    │   └── SKILL.md                  # Meal suggestion skill
    ├── add-to-shopping-list/
    │   └── SKILL.md                  # Shopping list management skill
    └── meal-planner/
        └── SKILL.md                  # Meal plan orchestrator skill
```

### User Data Structure (Your Project)

Your meal planning data uses a simple, portable file structure with markdown files that are both human-readable and machine-parseable:

```
my-meals/ (your project directory)
├── PROFILE.md                         # Your profile and preferences
├── recipes/                           # Recipe collection (each in its own folder)
│   ├── chicken-congee/
│   │   ├── chicken-congee.md         # Recipe markdown
│   │   ├── chicken-congee.html       # Recipe card HTML
│   │   └── chicken-congee.pdf        # Recipe card PDF
│   ├── chicken-leg-quarters-roasted-with-magic-potatoes-and-carrots/
│   │   ├── chicken-leg-quarters-roasted-with-magic-potatoes-and-carrots.md  # Original quick staple
│   │   ├── chicken-leg-quarters-roasted-with-magic-potatoes-and-carrots_precise.md  # Precise variant
│   │   ├── chicken-leg-quarters-roasted-with-magic-potatoes-and-carrots_precise.html  # Recipe card HTML
│   │   └── chicken-leg-quarters-roasted-with-magic-potatoes-and-carrots_precise.pdf   # Recipe card PDF
│   ├── lasagna-classic/
│   │   ├── lasagna-classic.md
│   │   ├── lasagna-classic.html
│   │   └── lasagna-classic.pdf
│   ├── thit-kho/
│   │   ├── thit-kho.md               # Personalized version (from research-recipe)
│   │   ├── thit-kho_simple.md        # Simple version variant (research)
│   │   ├── thit-kho_authentic.md     # Authentic version variant (research)
│   │   └── thit-kho_refined.md       # Refined version variant (research)
│   └── [recipe-name]/
│       ├── [recipe-name].md          # Recipe markdown
│       ├── [recipe-name]_[suffix].md # Recipe variant (optional, e.g., _precise, _vegetarian, _simple, _authentic, _refined)
│       ├── [recipe-name].html        # Recipe card HTML (optional)
│       ├── [recipe-name].pdf         # Recipe card PDF (optional)
│       └── [images]/                 # Future: recipe photos, step photos, etc.
├── meal-plans/                        # Meal plan archive
│   ├── 2025-12-16 to 2025-12-22.md  # Meal plans with embedded shopping lists
│   ├── 2025-12-23 to 2025-12-29.md
│   └── [YYYY-MM-DD to YYYY-MM-DD].md
└── shopping-lists/                    # Shopping lists by trip date
    ├── 2025-12-23.md                 # Shopping list for specific date
    ├── 2026-01-05.md
    └── [YYYY-MM-DD].md
```

### Recipe File Format

**Location**: `./recipes/[recipe-name]/[recipe-name].md`
**Naming convention**: Each recipe lives in its own folder. Folder and file names are lowercase, hyphenated, descriptive (e.g., `recipes/lasagna-classic/lasagna-classic.md`)

**Why folders?** Each recipe folder can contain:
- The recipe markdown file
- Generated recipe card HTML and PDF
- Future assets like photos, videos, or alternative versions

**Structure**:

```markdown
# [Recipe Title]

**Source:** [Source Name/Website]
**URL:** [Original Recipe URL]
**Cuisine:** [Cuisine Type]
**Category:** [soup/main-course/side-dish/dessert/etc.]
**Servings:** [Number]
**Total Time:** [HH:MM or "X hours Y minutes"]
**Active Time:** [HH:MM or "X minutes"] *(if available)*

## Description

[1-3 sentence description of the dish, its flavors, and appeal]

## Ingredients

| Quantity | Unit | Ingredient | Preparation |
|----------|------|------------|-------------|
| 500      | g    | pasta      | dried, any shape |
| 2        | whole | onions    | diced |
| 4        | cloves | garlic  | minced |
| 400      | ml   | crushed tomatoes | canned |
| -        | -    | salt       | to taste |
| 30       | ml   | olive oil  | extra virgin |

*Note: All measurements in metric. Use "-" for quantity/unit when "to taste" or not quantified.*

## Instructions

1. [First step with clear actions and any time/temperature details]
2. [Second step]
3. [Continue with numbered steps, one action per step when possible]
4. [Include temperatures in Celsius and times]
5. [Final plating or serving instructions]

## Notes from Source

- [Any tips, warnings, or variations mentioned in the original recipe]
- [Storage instructions]
- [Make-ahead notes]
- *(Leave empty if none provided)*

## Personal Notes

*Last made: [Date]*
*Rating: [1-5 stars or empty]*

- [Your modifications, observations, or feedback after cooking]
- [Timing notes: "Actually took 45 min not 30"]
- [Ingredient substitutions that worked]
- *(Empty until user adds notes)*

## Tags

[tag1] [tag2] [tag3] [tag4] [tag5] [tag6]

*Example tags: italian, pasta, weeknight, comfort-food, make-ahead, vegetarian*
```

**Key formatting rules**:
- **Measurements**: Always metric (ml, g, kg, °C)
- **Ingredient table**: Four columns (Quantity | Unit | Ingredient | Preparation)
- **Instructions**: Numbered list, one clear action per step
- **Tags**: Lowercase, hyphenated, space-separated
- **Temperatures**: Celsius (converted from Fahrenheit if needed)

---

### Recipe Variants

Recipes can have multiple variants stored in the same folder, each with a descriptive suffix starting with underscore:

**Variant naming**: `[recipe-name]_[suffix].md`

**Common variant types:**
- `_precise` - Quick staple recipe converted to exact measurements and detailed instructions for sharing
- `_simple` - Simplified version with accessible ingredients and easy techniques (from research-recipe)
- `_authentic` - Traditional version prioritizing cultural authenticity (from research-recipe)
- `_refined` - Chef-level version with advanced techniques (from research-recipe)
- `_vegetarian` / `_vegan` - Dietary adaptation
- `_gluten-free` / `_dairy-free` - Allergen-free version
- `_double` / `_scaled-12` - Scaled for different serving sizes
- `_grilled` / `_instant-pot` - Different cooking method
- `_simplified` - Easier or faster version
- Custom suffixes for any other modification

**Why use variants?**
- Keep original quick staple recipes as personal memory aids while creating detailed versions for sharing
- Preserve research from multiple sources when developing a recipe (simple, authentic, refined approaches)
- Maintain dietary adaptations without losing the original
- Document different scaling approaches when simple multiplication doesn't work
- Experiment with techniques while preserving the original method
- Learn from different perspectives on the same dish
- Each variant is independent and can evolve separately

**Example folders with variants:**

*Quick staple with precise variant:*
```
recipes/chicken-thighs-pan-fried-with-dirty-rice/
├── chicken-thighs-pan-fried-with-dirty-rice.md          # Original quick staple
├── chicken-thighs-pan-fried-with-dirty-rice_precise.md  # Detailed version for sharing
├── chicken-thighs-pan-fried-with-dirty-rice_double.md   # Doubled for guests
└── chicken-thighs-pan-fried-with-dirty-rice_precise.pdf # Recipe card from precise variant
```

*Researched recipe with multiple perspectives:*
```
recipes/thit-kho/
├── thit-kho.md               # Your personalized version (developed through research)
├── thit-kho_simple.md        # Simple version from research (accessible, quick)
├── thit-kho_authentic.md     # Authentic version from research (traditional family method)
└── thit-kho_refined.md       # Refined version from research (chef techniques)
```

**Relationship tracking:**
- Variants include a link back to the original recipe in Personal Notes
- Original recipes can optionally note available variants
- All related files live in the same folder for easy discovery

### Meal Plan File Format

**Location**: `./meal-plans/[YYYY-MM-DD] to [YYYY-MM-DD].md`
**Naming convention**: Date range in ISO format (e.g., `2025-12-16 to 2025-12-22.md`)

**Structure**:

```markdown
# Meal Plan: [Date Range]

**Created:** [YYYY-MM-DD]
**Status:** [Planning / Active / Completed]
**Type:** [Weekly / Monthly / Custom]

## Overview

**Planning notes:**
- [Why this plan: using up ingredients, centered around specific recipe, etc.]
- [Special considerations: guests, holidays, busy week, etc.]

**Goals for this plan:**
- [e.g., "Use up leftover chicken and kale"]
- [e.g., "Try the new Thai curry recipe"]
- [e.g., "Keep weeknights under 30 minutes"]

## Meal Schedule

### Monday, YYYY-MM-DD
**Dinner:** [Recipe Name](../recipes/recipe-filename.md)
- Servings: [X]
- Prep time: [X minutes]
- Notes: [Any specific notes for this instance]

### Tuesday, YYYY-MM-DD
**Dinner:** [Recipe Name](../recipes/recipe-filename.md)
- Servings: [X]
- Prep time: [X minutes]
- Notes: [e.g., "Marinate in the morning"]

### Wednesday, YYYY-MM-DD
**Dinner:** [Recipe Name](../recipes/recipe-filename.md)
- Servings: [X]
- Prep time: [X minutes]

[Continue for all days in plan]

## Shopping List

### Items We Already Have

**Pantry staples** (from profile):
- Olive oil, salt, black pepper, garlic powder, etc.

**Ingredients to use up** (from previous meal plans):
- 200g leftover chicken (from 2025-12-12 plan)
- 1 bunch kale (from 2025-12-15 plan)
- 3 cloves garlic

---

### Items to Purchase

#### Publix (Main Shop - Saturday, 2025-12-16)

**Produce**
- [ ] 2 whole onions
- [ ] 3 whole bell peppers (red)
- [ ] 1 bunch fresh basil
- [ ] 500g button mushrooms
- [ ] 2 whole lemons

**Meat & Seafood**
- [ ] 1kg chicken breast
- [ ] 500g ground beef (90% lean)

**Dairy & Eggs**
- [ ] 500ml heavy cream
- [ ] 200g parmesan cheese (block, not pre-grated)
- [ ] 1 dozen eggs

**Pantry & Dry Goods**
- [ ] 500g pasta (penne)
- [ ] 800ml crushed tomatoes (canned)
- [ ] 400ml coconut milk

**Frozen**
- [ ] 500g peas

**Estimated cost:** $XX-XX

#### Corner Store (If Needed - Wednesday)

**Produce**
- [ ] 1 whole avocado (if making Tuesday's recipe and need fresh)

---

## Prep Schedule

**Sunday (Prep Day):**
- [ ] Marinate chicken for Monday's dinner
- [ ] Chop onions and peppers, store in containers
- [ ] Make sauce for Wednesday's pasta (can be done ahead)

**Morning Of:**
- Monday: Nothing needed
- Tuesday: Take chicken out of fridge 30 min before cooking
- Wednesday: Defrost sauce if frozen

## Post-Plan Feedback

*To be filled out after completing the meal plan*

### Recipe Ratings

**[Recipe Name]** (Monday)
- Rating: ⭐⭐⭐⭐⭐
- Feedback: [What worked, what didn't, would you make again?]
- Adjustments: [Any changes you made]

**[Recipe Name]** (Tuesday)
- Rating:
- Feedback:
- Adjustments:

[Continue for all recipes]

### Leftover Ingredients

*Record ingredients purchased but not fully used, to prioritize in next plan:*

- [ ] [Quantity] [unit] [ingredient] - [Condition/expiration estimate]
- [ ] 100g parmesan cheese - good for 2 weeks
- [ ] 3 cloves garlic - good for 1 week
- [ ] 1/2 bunch basil - use within 3 days

### Overall Plan Assessment

- **What worked well:**
  - [e.g., "Prep day saved tons of time on weeknights"]

- **What to improve:**
  - [e.g., "Underestimated how long the Tuesday recipe would take"]

- **Recipes to repeat:**
  - [Recipe names]

- **Recipes to skip next time:**
  - [Recipe names and why]

### Profile Updates

*Preferences or information learned that should update the profile:*

- [e.g., "Actually loves spicy food more than initially stated"]
- [e.g., "Discovered they don't like the texture of eggplant"]
```

**Key formatting rules**:
- **Filename**: ISO date format for the range
- **Recipe links**: Relative paths to recipe files using markdown links
- **Shopping lists**: Organized by store, then by section, with checkboxes
- **Status tracking**: Clear indication of planning stage
- **Feedback section**: Completed after the plan is executed

### Shopping List File Format (Standalone)

**Location**: `./shopping-lists/[YYYY-MM-DD].md`
**Naming convention**: Date of shopping trip (when you shop, not when you cook)
**Purpose**: Track ingredients needed for meals, with smart quantity allocation

Shopping lists are created and managed by the `add-to-shopping-list` skill, which handles:
- Smart allocation (claims from existing purchases to avoid duplicates)
- Quantity tracking (purchased vs. claimed by meals)
- Appropriate shopping trip determination
- Store and section organization
- Pantry staple filtering

**Structure**:

```markdown
# Shopping List: [Month Day, Year]

**Shopping Date:** [Day of Week], [Month Day, Year]
**Stores:** [List of stores for this trip]
**For Meals:** [List dates/meals this shopping supports]

---

## [Store Name] (e.g., Rewe, Costco, Asian Market)

### Produce
- [ ] [Item name] ([quantity]) - *for [meal name] ([amount used]), [amount remaining] remaining*
- [ ] [Item name] ([quantity]) - *for [meal 1] ([amount]), [meal 2] ([amount]), [amount remaining] remaining*

### Meat & Seafood
- [ ] [Item name] ([quantity]) - *for [meal name]*

### Dairy & Eggs
- [ ] [Item name] ([quantity]) - *for [meal 1] ([amount]), [meal 2] ([amount])*

### Baking / Dry Goods
- [ ] [Item name] ([quantity]) - *for [meal name], extra for pantry*

### Frozen
- [ ] [Item name] ([quantity]) - *for [meal name]*

### Other
- [ ] [Item name] ([quantity])

---

## [Another Store Name]

[Same section structure]

---

## Notes

- [Any special shopping notes]
- [Substitution options]
- [Store-specific reminders]

---

**Items assumed on hand** (verify if needed):
- [List of pantry staples not added to list]
- [List of items user confirmed they have]

*If you need any of these items, add them to the appropriate section above.*
```

**Key features:**
- **Quantity tracking**: Shows how much is purchased and how much each meal claims
  - Example: `Rice (500g bag) - *for Monday stir-fry (200g), Wednesday fried rice (200g), 100g remaining*`
- **Smart allocation**: If a meal needs rice and rice is already being purchased, it just claims more of that bag
- **Realistic packages**: Accounts for actual package sizes (can't buy 50g flour, must buy 1kg bag)
- **Unclaimed tracking**: Shows what's left over for future use
- **Pantry awareness**: Filters out items always on hand, confirms "usually have" items

## Getting Started

### Initial Setup

1. **Install this plugin** in Claude Code (if not already installed)

2. **Create your meal planning project directory**
```bash
   mkdir my-meals
   cd my-meals
   mkdir recipes meal-plans shopping-lists
```

3. **Build your profile**
  - Use the `build-profile` skill to create your initial `PROFILE.md`
  - Or manually create `PROFILE.md` using the template above
  - Answer questions about servings, tastes, restrictions, shopping habits, etc.

3. **Import your first recipes**
  - Use the `import-recipe` skill with recipe URLs
  - Or manually create recipe files using the format above
  - Start with 10-15 favorite recipes to build a foundation

4. **Create your first meal plan**
  - Use the `create-meal-plan` skill
  - Specify your date range (e.g., "next week")
  - Review and adjust the proposed meals
  - Generate the shopping list

5. **Go shopping**
  - Use the checklist in your meal plan
  - Check off items as you shop
  - Note any substitutions or unavailable items

6. **Cook and capture feedback**
  - Follow your meal plan
  - Add notes to recipe files as you cook
  - After the week, use `capture-feedback` to record insights

### Ongoing Usage

**Weekly workflow:**
1. **Review previous plan** (5 minutes)
  - Note leftover ingredients
  - Rate recipes and add feedback

2. **Generate new plan** (10 minutes)
  - Use `create-meal-plan` with preferences
  - Consider leftovers and ingredients to use up
  - Adjust based on the upcoming week's schedule

3. **Shop** (varies)
  - Follow organized shopping list
  - Check off items as you go

4. **Cook and enjoy**
  - Reference recipes from meal plan
  - Add notes about timing, substitutions, etc.

## Workflow Examples

### Example 1: Standard Weekly Plan

**Scenario**: User wants a standard week of dinners for 2 people.

```
User: "Create a meal plan for next week. I'm free to shop on Saturday."

Agent: [Reads PROFILE.md]
Agent: [Uses create-meal-plan skill]
  - Considers: 2 adults, dietary restrictions (no shellfish), favorite cuisines
  - Checks: Leftover ingredients from last plan (kale, chicken)
  - Balances: Variety, cooking time (weeknights < 45 min), nutrition
  - Generates: 7 dinner recipes with shopping list organized for Saturday Publix trip

Output: meal-plans/2025-12-23 to 2025-12-29.md
```

### Example 2: Using Up Ingredients

**Scenario**: User has specific ingredients they need to use up.

```
User: "I have 3 bell peppers and half a bag of rice that need to be used. Build a plan around those."

Agent: [Reads PROFILE.md]
Agent: [Searches recipes with bell peppers and rice]
Agent: [Uses create-meal-plan skill with prioritization]
  - Finds: Stuffed peppers recipe, fried rice, stir-fry
  - Plans: 3 meals using those ingredients prominently
  - Adds: 4 other meals for variety
  - Generates: Shopping list excluding bell peppers and rice

Output: meal-plans/2025-12-23 to 2025-12-29.md (with "using up ingredients" note)
```

### Example 3: Recipe-Centered Plan

**Scenario**: User found a recipe they want to try and wants meals to complement it.

```
User: "I want to make this recipe on Saturday [URL]. Build a week around it."

Agent: [Uses import-recipe to save the new recipe]
Agent: [Reads PROFILE.md]
Agent: [Uses create-meal-plan with anchor recipe]
  - Anchors: New recipe on Saturday (longer cook time OK)
  - Complements: Chooses other recipes that share ingredients to minimize waste
  - Balances: Variety in cuisines and cooking methods
  - Optimizes: Shopping list to get all ingredients in one trip

Output: recipes/[new-recipe]/[new-recipe].md + meal-plans/2025-12-23 to 2025-12-29.md
```

### Example 4: Quick Weeknight Focus

**Scenario**: User has a busy week and needs fast meals.

```
User: "I have a crazy week. Only give me recipes under 30 minutes."

Agent: [Reads PROFILE.md]
Agent: [Searches recipes filtered by active time < 30 min]
Agent: [Uses create-meal-plan with constraint]
  - Filters: Only quick recipes or slow-cooker recipes (low active time)
  - Suggests: Prep day on Sunday to make weeknights easier
  - Generates: Plan with 5 quick dinners + prep instructions

Output: meal-plans/2025-12-23 to 2025-12-27.md (5-day week, quick meals)
```

### Example 5: Post-Plan Feedback Loop

**Scenario**: User completed a meal plan and wants to give feedback.

```
User: "Let's review last week's meal plan."

Agent: [Uses capture-feedback skill]
Agent: [Reads meal-plans/2025-12-16 to 2025-12-22.md]
Agent: [Interviews user about each recipe]
  - Asks: "How was [Recipe]? Would you make it again?"
  - Records: Ratings, specific feedback, leftover ingredients
  - Updates: Recipe files with personal notes
  - Updates: PROFILE.md with discovered preferences

Output: Updated meal plan file with feedback section + updated PROFILE.md
```

### Example 6: Creating a Printable Recipe Card

**Scenario**: User wants to print a recipe card to use in the kitchen or share with a friend.

```
User: "Create a recipe card for the chicken congee recipe."

Agent: [Uses recipe-card skill]
Agent: [Finds recipes/chicken-congee.md]
Agent: [Parses recipe data]
  - Extracts: Title, metadata, ingredients, instructions, notes
  - Formats: Clean HTML with print-optimized styling
  - Creates: recipes/chicken-congee/chicken-congee.html
  - Generates PDF: recipes/chicken-congee/chicken-congee.pdf (using Chrome headless)

Output:
- recipes/chicken-congee/chicken-congee.md (recipe markdown)
- recipes/chicken-congee/chicken-congee.html (recipe card HTML)
- recipes/chicken-congee/chicken-congee.pdf (recipe card PDF)
```

## Advanced Features

### Seasonal Planning

The system can consider seasonal ingredients to:
- Suggest recipes featuring in-season produce
- Highlight cost savings on seasonal items
- Support local/farmers market shopping
- Adjust plans by time of year (hearty winter vs. light summer)

### Batch Cooking & Meal Prep

For users who prefer meal prep:
- Identify recipes that scale well
- Suggest Sunday prep tasks that save weeknight time
- Plan recipes that share prep work (chopped onions for 3 recipes)
- Note which components can be prepped ahead

### Budget Optimization

Track costs and optimize spending:
- Estimate total meal plan cost
- Suggest budget-friendly alternatives
- Highlight expensive recipes for special occasions
- Track spending trends over time

### Nutritional Insights

Support health goals without medical advice:
- Estimate macros and calories per recipe
- Balance meal plans for nutritional variety
- Highlight protein, fiber, or other nutrients of interest
- Support stated dietary patterns (Mediterranean, high-protein, etc.)

### Smart Substitutions

Help with ingredient flexibility:
- Suggest swaps for allergies or preferences
- Offer alternatives when items are unavailable
- Provide conversion ratios for substitutions
- Note which substitutions affect flavor vs. texture

### Multi-Week Planning

Plan beyond a single week:
- Generate monthly meal rotations
- Avoid repeat fatigue with intelligent variety
- Plan bulk shopping trips vs. weekly trips
- Track favorite recipes to ensure regular rotation

### Integration & Export

Make plans portable and shareable:
- Export shopping lists to mobile-friendly formats
- Generate printable meal plans
- Create calendar events for meal prep and cooking
- Share favorite recipes with friends/family

### Learning & Adaptation

The system improves over time by:
- Tracking which recipes get repeated (proven favorites)
- Learning time estimate accuracy (does 30 min recipe really take 45?)
- Discovering hidden preferences from feedback
- Adjusting serving size recommendations based on leftover patterns
- Refining shopping list organization based on user's actual shopping flow

---

## Contributing

This plugin follows the **Agent Skills Open Standard**. To add new skills:

1. Create a new directory under `skills/[skill-name]/`
2. Add a `SKILL.md` file following the standard format:
```markdown
   ---
   name: skill-name
   description: Brief description of what the skill does
   ---

   # [Skill Name] Workflow

   ## Step 1: [First Step]
   [Detailed instructions]

   ## Step 2: [Second Step]
   [Detailed instructions]
```
3. Test the skill with various scenarios
4. Update this README with the new skill documentation

## License

This project and its skills are open source. See individual skill files for specific license information.

---

**Last updated:** 2025-12-22
