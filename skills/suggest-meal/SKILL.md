---
name: suggest-meal
description: Suggest a complete meal (main + sides) for a specific date and time, with recipe discovery
---

# Suggest Meal Workflow

This skill helps you plan a single meal for a specific date and time. It considers your profile, what you have on hand, your schedule, and your recipe collection to suggest a complete meal (main dish + appropriate sides). If you don't have the perfect recipe, it will search the web and help you import new recipes or create quick staples.

## Overview

When you ask for meal suggestions, this skill will:
1. Verify the exact date and day of week you're asking about
2. Check if a meal plan already exists for that date
3. Consider your context (people, leftovers, schedule, ingredients on hand)
4. Search your recipe collection for matches OR find new recipes on the web
5. Suggest appropriate side dishes to complete the meal
6. Get your approval and optionally add to a meal plan
7. Provide a complete ingredient list for shopping

This is perfect for planning individual meals without creating a full week-long plan.

---

## Step 1: Verify Date and Day of Week

**CRITICAL: Use the Bash tool to verify today's date and calculate the target date.**

Ask the user what date or day they're asking about. They might say:
- "tonight"
- "tomorrow"
- "Wednesday"
- "next Saturday"
- "January 15"
- etc.

Use Bash to get today's date and calculate the target:

```bash
# Get today's date
date '+%Y-%m-%d %A'

# For relative dates, use date calculations
# Tomorrow:
date -v+1d '+%Y-%m-%d %A'

# Next Wednesday (example):
date -v+wed '+%Y-%m-%d %A'

# Specific date:
date -j -f '%B %d' 'January 15' '+%Y-%m-%d %A' 2>/dev/null || date -d 'January 15' '+%Y-%m-%d %A'
```

**Confirm with the user:**
"I understand you're asking about [Day of Week], [Month Day, Year]. Is that correct?"

If not correct, clarify and recalculate.

---

## Step 2: Check for Existing Meal Plan

Use Glob to find meal plans:

```
Pattern: "meal-plans/*.md"
```

Look for a meal plan file that covers the target date. Meal plan filenames are formatted as `YYYY-MM-DD to YYYY-MM-DD.md`.

**If a meal plan exists for that date:**

Read the meal plan file and check if the requested meal (dinner, lunch, etc.) is already planned for that day.

**If meal is already planned:**
"I found your meal plan for that week. You have [Recipe Name] planned for [Day] [Meal]. Would you like to:
1. Stick with this plan (I'll show you the recipe links)
2. Swap it out for something else
3. Add a different meal time (if they asked for lunch but only dinner is planned)"

**If user chooses to stick with the plan:**
- Show the main dish name and link
- Show the side dishes with links (if recipes) or descriptions
- Skip to Step 9 (provide ingredient list)

**If user wants to swap or no meal is planned:**
- Continue to Step 3

**If no meal plan exists:**
- Note that we'll create a meal suggestion, and ask if they want to add it to a new meal plan later
- Continue to Step 3

---

## Step 3: Read Profile for Context

**Read `PROFILE.md`** to understand:
- Household size and appetite adjustments
- Dietary restrictions (ALWAYS respect these)
- Favorite cuisines and cooking style
- Skill level and available equipment
- Pantry staples
- Wednesday guests or other recurring events
- Shopping patterns

This informs all meal suggestions.

---

## Step 4: Gather Meal Context

Ask the user about the specific meal context. Use AskUserQuestion for efficiency.

**Essential questions:**

1. **What meal?** "Is this for dinner, lunch, or another meal?" (Default: dinner)

2. **How many people?** "How many people are you serving?" (Default: from profile, adjust for Wednesday if applicable)

3. **Leftovers?** "Do you want leftovers, or cooking for exact portions?" (Options: "Want leftovers", "Exact portions only", "Flexible")

4. **Time available?** "How much time do you have for cooking?" (Options: "Under 30 min", "30-60 min", "1-2 hours", "2+ hours / special meal")

5. **Ingredients on hand?** "Do you have specific ingredients you want to use up?" (They can list items or say "no, I'll shop")

6. **Scheduled grocery trip?** "Do you have a grocery trip or delivery scheduled before this meal where you can add ingredients?" (Yes/No, when)

7. **Special considerations?** "Any special considerations? (Theme, dietary needs for guests, specific cravings, etc.)" (Optional, can be "none")

**Additional context to consider:**

Ask about adjacent meals if relevant:
- "What did you have the night before, if you remember?"
- "Do you have meals planned for the next few days that I should coordinate with?"

This helps avoid repetition and create ingredient efficiency.

---

## Step 5: Search Recipe Collection for Main Dish

Now search your recipe collection based on the gathered context.

**Search strategy based on time available:**

*Under 30 min:*
```
Grep pattern: "\[quick-staple\]|\[quick\]|\[under-30-min\]"
Path: recipes/
Output: files_with_matches
```

*30-60 min:*
```
Grep pattern: "\[weeknight\]|\[under-60-min\]|\[quick-staple\]"
Path: recipes/
Output: files_with_matches
```

*1-2 hours:*
```
Grep pattern: "\[main-course\]"
Path: recipes/
Output: files_with_matches
```

*2+ hours / special meal:*
```
Grep pattern: "\[featured-dish\]|\[special-occasion\]|\[sunday-dinner\]"
Path: recipes/
Output: files_with_matches
```

**Also filter by:**
- Cuisine preferences (if user mentioned a preference)
- Ingredients on hand (search for those ingredients)
- Dietary restrictions (exclude restricted items)
- Recent meals (avoid what they just had)

**Read top 5-10 candidate recipes** to evaluate:
- Does it fit the time constraint?
- Does it use ingredients they have on hand?
- Does it fit the day/meal context?
- Is it appropriate for the number of people?
- Does it match their cooking style and skill level?

---

## Step 6: Determine if Collection Has Good Match

**If you found 1-3 strong matches in their collection:**
- Proceed to Step 7 (suggest sides)
- Present collection recipes as options

**If you found NO strong matches or only weak matches:**
- Note the best match from their collection (if any)
- Proceed to Step 6a (web search for recipes)

---

## Step 6a: Web Search for New Recipe Options

If the user's collection doesn't have a perfect match, search the web for recipes.

**Search strategy:**

Use WebSearch to find recipes that match:
- The meal type and time constraint
- Their cooking style (from profile: comfort food, from-scratch, fundamental techniques)
- Their skill level (advanced home chef in their case)
- Their favorite cuisines
- Any specific requirements (ingredients to use up, dietary needs, etc.)

**Search query examples:**
- "best [cuisine] [dish type] recipe [time constraint]"
- "highly rated [dish] recipe using [ingredient on hand]"
- "[cuisine] [dish] recipe from scratch"

**Important:** Look for:
- High-rated recipes from reputable sources
- Recipes that match their cooking philosophy (avoid shortcuts, pre-mixed spices, processed ingredients per their profile)
- Recipes from skilled home cooks or chefs
- Clear instructions appropriate for their skill level

**Find at least 3 options** (ideally 4: 3 web options + 1 best from collection)

For each option, use WebFetch to get full recipe details:

```
WebFetch URL with prompt: "Extract the complete recipe information including: recipe title, source/author, cuisine type, servings, total time, active time, description, all ingredients with quantities, all instruction steps in order, and any tips or notes about technique or variations."
```

---

## Step 6b: Present Recipe Options to User

Present the recipes in a clear comparison format:

```markdown
# Recipe Options for [Day of Week] [Meal]

Based on your requirements ([time constraint], [people count], [special considerations]), here are the best options I found:

## Option 1: [Recipe Name] ⭐ RECOMMENDED

**Source:** [From your collection OR Web source]
**Why I recommend this:** [Explanation of why this is the top choice - matches their adventurousness, fits requirements perfectly, uses ingredients on hand, etc.]
**Cuisine:** [Cuisine]
**Time:** [Total time] ([Active time] active)
**Servings:** [Servings] (scales easily for [their portion count])
**Key ingredients:** [List main ingredients]
**What makes it great:** [Brief compelling description]

## Option 2: [Recipe Name]

**Source:** [Source]
**Why this works:** [Explanation]
[Same structure as Option 1]

## Option 3: [Recipe Name]

**Source:** [Source]
**Why this works:** [Explanation]
[Same structure as Option 1]

## Option 4: [Recipe from Your Collection] (Closest match)

**Source:** Your recipe collection
**Why this works:** [Explanation of how it fits, any compromises]
[Same structure]

---

**My recommendation:** Option 1 ([Recipe Name]) because [detailed reasoning about why it's the best fit for their style, requirements, and preferences].

**Questions:**
1. Which option appeals to you most?
2. Would you like to modify any of these?
3. Should I suggest a different direction entirely?
```

**Wait for user to choose** or provide feedback.

**If user chooses an option from the web:**
- Proceed to import it using the import-recipe skill
- Then continue to Step 7 (suggest sides)

**If user wants to create a quick staple instead:**
- Use the quick-staple skill to capture it
- Then continue to Step 7 (suggest sides)

**If user chooses option from their collection:**
- Continue to Step 7 (suggest sides)

---

## Step 7: Suggest Appropriate Side Dishes

Now suggest side dishes that complement the main dish.

**Considerations for sides:**

1. **Does the main dish already include sides?**
   - Complete meals (pasta with sauce, stir-fry with rice, soup with bread) may not need additional sides
   - Protein-only mains (roast chicken, grilled steak, pan-fried fish) definitely need sides

2. **What's the cuisine and flavor profile?**
   - Italian main → roasted vegetables, simple salad, crusty bread
   - Asian main → rice, stir-fried vegetables, simple cucumber salad
   - German main → potatoes (roasted/boiled/mashed), cabbage, sauerkraut
   - American comfort food → mashed potatoes, roasted vegetables, bread
   - French main → roasted vegetables, potatoes au gratin, green salad

3. **What's the cooking method and timing?**
   - If main uses oven, sides can roast alongside
   - If main is stovetop, oven sides work well
   - If time is tight, use quick sides (steamed, boiled, simple salad)

4. **What sides does the user have in their collection?**

Search for side dish recipes:
```
Grep pattern: "\[side-dish\]|\[vegetable\]|\[salad\]|\[starch\]"
Path: recipes/
Output: files_with_matches
```

**Read any side dish recipes they have** to see if they fit.

**Balance variety:**
- If user has several side recipes, prefer those
- If user has few side recipes, use simple sides without recipes more often
- Don't suggest the same side dish repeatedly

**Suggest 1-2 sides:**
- Usually 1 vegetable + 1 starch, OR
- 1 vegetable if main includes starch, OR
- Just note "complete meal" if main is self-contained

**Format side suggestions:**

```markdown
## Suggested Sides for [Main Dish Name]

To complete this meal, I recommend:

**Vegetable Side:** [Name]
- [Brief description: "Roasted broccoli - toss with olive oil, salt, pepper; roast 20 min at 220°C"]
- **Why this works:** [Complements the flavors, uses available oven space, quick preparation, etc.]
- **From:** [Your collection: link OR Simple side (no recipe needed)]

**Starch Side:** [Name]
- [Brief description: "Mashed potatoes - boil 20 min, mash with butter and milk"]
- **Why this works:** [Comfort pairing, soaks up sauce, traditional accompaniment, etc.]
- **From:** [Your collection: link OR Simple side (no recipe needed)]

**Total meal timing:** [Main time] + [Side prep overlaps/adds X minutes] = ~[Total] minutes

---

**Questions:**
1. Are you comfortable with these simple side descriptions, or would you like me to find full recipes for them?
2. Would you prefer different sides?
3. If I'm suggesting simple sides without recipes, would you like me to save them as quick staples for future reference?
```

**Wait for user response.**

**If user wants full recipes for sides:**
- Use WebSearch to find highly rated side dish recipes
- Use WebFetch to get details
- Use import-recipe skill to import them
- Update the side suggestions with links to imported recipes

**If user is comfortable with simple descriptions:**
- Ask: "Would you like me to save [side name] as a quick staple with the [side-dish] tag so you have it in your collection?"
- If yes, use quick-staple skill to save it with [side-dish] tag
- If no, continue with the simple description

**If user wants different sides:**
- Take their feedback and suggest alternatives
- Repeat this step

---

## Step 8: Present Complete Meal for Approval

Once you have main dish + sides approved, present the complete meal:

```markdown
# Complete Meal for [Day of Week], [Month Day]

## Main Dish
**[Recipe Name]**
[Link to recipe if it exists, or note "Quick staple - see description"]

**Timing:** ~[X] minutes ([Y] active time)
**Serves:** [Number of people] [with/without leftovers as requested]

## Sides

**[Vegetable Side Name]**
- [Description with cooking instructions OR link to recipe]
- Timing: [X] minutes (can cook while [relationship to main])

**[Starch Side Name]** (if applicable)
- [Description with cooking instructions OR link to recipe]
- Timing: [X] minutes (can cook while [relationship to main])

## Total Meal Timing
**Active time:** ~[X] minutes
**Total time:** ~[X] minutes
*[Note about what can be done simultaneously]*

## Flavor Profile
[Brief description of how the dishes work together - e.g., "Rich, savory main with light, fresh vegetable side and creamy starch for balance"]

---

**Is this meal approved?**
- If yes, would you like me to add it to a meal plan?
- If no, what would you like to adjust?
```

**Wait for approval.**

**If not approved:** Take feedback and iterate (back to Step 6 or 7 depending on what needs changing)

**If approved:** Continue to Step 9

---

## Step 9: Add to Meal Plan (Optional)

Ask the user: "Would you like me to add this meal to a meal plan?"

**If yes:**

Check if a meal plan exists for that date range (from Step 2).

**If meal plan exists:**
- Use Edit tool to add or update the meal in the existing meal plan
- Add the meal following the meal plan template format
- Include main dish with link, sides with descriptions/links, timing, and notes

**If no meal plan exists:**
Ask: "Should I create a new meal plan for this date? What date range should it cover?"
- Typically: the week containing this date (find the Saturday-Friday or Sunday-Saturday range)
- Use Write tool to create a new meal plan file with just this one meal
- User can fill in other days later or use meal-planner skill for full week

**Confirm:** "I've added [Meal] to your meal plan for [Day], [Date]."

---

## Step 10: Provide Complete Ingredient List

Generate a complete ingredient list for the meal based on:
- Main dish recipe ingredients (scaled to serving size)
- Side dish recipe ingredients (if recipes exist) OR inferred ingredients for simple sides
- The number of servings requested

**Format:**

```markdown
# Complete Ingredient List for [Day] [Meal]

## For Main Dish: [Recipe Name]

### Produce
- [Item] ([quantity for X servings])
- [Item] ([quantity for X servings])

### Meat & Seafood
- [Item] ([quantity for X servings])

### Dairy & Eggs
- [Item] ([quantity for X servings])

### Dry Goods & Pantry
- [Item] ([quantity for X servings])

### Condiments & Sauces
- [Item] ([quantity for X servings])

## For Sides

### [Vegetable Side Name]
- [Item] ([quantity]) - *[e.g., "500g broccoli"]*
- Olive oil, salt, pepper (from pantry staples)

### [Starch Side Name] (if applicable)
- [Item] ([quantity]) - *[e.g., "1kg potatoes"]*
- Butter, milk (from pantry staples)

## Already Have (From Pantry Staples)
- [List items that are pantry staples per profile]

## Need to Purchase
[Consolidated list of items NOT in pantry staples]

---

**For your scheduled [grocery trip/delivery on Date]:**
[Clean list of just the items to add to shopping list]

**Estimated additional cost:** €[X-Y] (rough estimate)
```

**This ingredient list can be used by:**
- The user for manual shopping list creation
- Other skills to add items to meal plan shopping lists
- Integration with future shopping list management features

---

## Step 11: Confirm Completion

Provide a final summary:

```markdown
# Meal Suggestion Complete!

**[Day of Week], [Month Day] - [Meal]**

**Main:** [Recipe Name] ([link or "Quick staple"])
**Sides:** [Side 1], [Side 2]
**Total time:** ~[X] minutes
**Serves:** [Number] people [with/without leftovers]

**Status:**
✓ Main dish [from collection / imported from web / saved as quick staple]
✓ Sides [from collection / simple descriptions / imported from web / saved as quick staples]
✓ [Added to meal plan for [date range] / Not added to meal plan]
✓ Complete ingredient list provided

**Next steps:**
- [Add ingredients to your shopping list for [scheduled trip]]
- [Review the recipe before cooking]
- [Enjoy your meal!]

**Need changes?** Let me know and I can adjust the meal, swap sides, or modify anything else.
```

---

## Important Guidelines

### Date Verification
- **ALWAYS verify dates using Bash date commands** - never guess or rely on LLM date arithmetic
- Confirm the day of week and date with the user before proceeding
- If there's any confusion, ask for clarification

### Recipe Selection Philosophy
- **Prioritize user's collection first** for mains - only search web if no good match
- **Prefer simple sides** without recipes unless user has saved side dish recipes
- **Match user's cooking style** from profile (from-scratch, fundamental techniques, no shortcuts)
- **Consider skill level** (they're advanced, so don't shy away from technique)
- **Respect adventurousness** (they try new things weekly, but also value familiar staples)

### Side Dish Guidelines
- **Must complement main dish flavor profile** - this is most important
- **Must fit time constraints** - don't suggest 1-hour side for 30-min meal
- **Variety matters** - don't suggest same sides repeatedly
- **Simple is often better** - roasted vegetables with oil/salt/pepper don't need recipes
- **Offer to save simple sides as quick staples** with [side-dish] tag for future reference

### Web Recipe Search Quality
- Look for highly rated recipes (4+ stars, many reviews)
- Prefer recipes from:
  - Skilled home cooks or food bloggers
  - Professional chefs with accessible recipes
  - Reputable cooking sites (Serious Eats, NYT Cooking, etc.)
  - Cultural authorities for ethnic cuisines
- Avoid recipes with:
  - Shortcuts they don't like (canned soup, spice packets, etc.)
  - Overly processed ingredients
  - Poor technique or vague instructions

### Meal Plan Integration
- **Check for existing meal plans first** - don't create duplicates
- **Respect existing plans** - ask before overwriting
- **Format consistently** with meal-planner skill output
- **Include all details** - main, sides, timing, notes

### Dietary Restrictions
- **ALWAYS respect** dietary restrictions from profile
- **For guests,** ask if any restrictions apply for this specific meal
- **Never suggest** restricted items, even as optional

### Ingredient List Accuracy
- **Scale quantities** appropriately for serving count
- **Consolidate duplicates** if ingredient used in multiple components
- **Mark pantry staples** clearly so user knows what they already have
- **Provide actionable shopping list** ready to use

---

## Integration with Other Skills

**This skill works with:**
- **import-recipe**: When user chooses web recipe to import
- **quick-staple**: When user wants to save a simple recipe or side dish
- **meal-planner**: Reads existing meal plans, can add meals to plans
- **research-recipe**: If user wants deep research on a specific dish (suggest this if appropriate)

**This skill provides data for:**
- Shopping list management (ingredient lists)
- Meal plan updates (adding individual meals)
- Recipe collection growth (importing new recipes)

---

## Example Usage Flow

**User:** "What should I make for dinner tomorrow?"

**Assistant:** [Uses Bash to verify tomorrow is Wednesday, January 8, 2026]
"I understand you're asking about Wednesday, January 8, 2026. Is that correct?"

**User:** "Yes"

**Assistant:** [Checks meal plans, finds 2026-01-03 to 2026-01-11.md]
"I found your meal plan for that week. You have Chicken and Dumplings planned for Wednesday dinner (board gaming night). Would you like to stick with this plan or swap it out?"

**User:** "Oh right, stick with it"

**Assistant:** [Reads meal plan, extracts Wednesday meal]
"Great! Here's your planned meal for Wednesday:

**Main:** Chicken and Dumplings, Southern Style - Slow Cooker
- [Link to recipe]
- 6-8 hours slow cooker + 30 min stovetop finishing
- Perfect for board gaming group (5-7 people)

**Sides:** Complete meal (includes vegetables in broth) + Crusty bread

[Provides complete ingredient list from meal plan]

All set!"

---

**User:** "What should I make for dinner on Saturday?"

**Assistant:** [Uses Bash to verify Saturday is January 11, 2026]
"You're asking about Saturday, January 11, 2026, correct?"

**User:** "Yes"

**Assistant:** [Checks meal plan, finds Mac and Cheese with Hot Dogs planned]
"I found your meal plan - you have Mac and Cheese with Hot Dogs planned. Want to stick with that or change it?"

**User:** "Let's change it to something more interesting"

**Assistant:** [Gathers context through questions]
"Let me help you find something better for Saturday.

- How many people? [Default: 2]
- Time available? [Options shown]
- Ingredients to use up? [User lists or says no]
- Special considerations? [User provides or says none]"

[Searches recipe collection, finds strong matches]

"Based on your requirements, here are your best options from your collection:

**Option 1: Thịt Kho (Vietnamese Braised Pork & Eggs)** ⭐ RECOMMENDED
[Details, timing, why it's recommended]

**Option 2: Roast Chicken**
[Details, why it works]

**Option 3: Pasta with Red Sauce**
[Details, why it works]

My recommendation: Thịt Kho because you haven't made it recently, you have time on Saturday, and it's a special featured dish that's perfect for weekend cooking."

**User:** "Let's do the Thịt Kho"

**Assistant:** [Suggests sides]
"Perfect! To complete the meal, I recommend:

**Sides:**
- Steamed white rice (cook 1 cup rice in 2 cups water, 18 min)
- Simple cabbage slaw (shredded cabbage, vinegar, oil, salt, sugar - 5 min)

These are traditional accompaniments that let the rich pork and egg dish shine.

Are you comfortable with these simple descriptions, or would you like full recipes?"

**User:** "Simple descriptions are fine"

**Assistant:** [Presents complete meal for approval, user approves, adds to meal plan, provides ingredient list]

"Meal suggestion complete! I've updated your meal plan for Saturday with Thịt Kho + rice + slaw. Here's your ingredient list to add to your shopping..."

---

## Skill Complete

The suggest-meal skill provides personalized, context-aware meal suggestions for individual meals, with seamless integration into meal plans and support for recipe discovery when needed.
