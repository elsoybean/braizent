---
name: meal-planner
description: Create personalized meal plans with intelligent recipe selection and shopping lists
---

# Meal Planner Workflow

This skill helps you create thoughtful, personalized meal plans that consider your schedule, preferences, ingredient efficiency, and cooking goals. It's the central orchestrator of the meal planning system - bringing together your profile, recipe collection, and real-world constraints to create a realistic, exciting plan.

## Overview

When you ask to plan meals, this skill will:
1. Gather your goals and constraints for the planning period
2. Read your profile for context and preferences
3. For each meal, use the **suggest-meal** skill to find the right recipe
4. Get your approval for each meal before adding it to the plan
5. Use the **add-to-shopping-list** skill to add ingredients incrementally
6. Create a complete meal plan file with schedule and prep notes
7. Present the consolidated shopping lists at the end

This is a collaborative, iterative process - the goal is to create a plan that excites you and feels realistic for your life.

---

## Step 1: Read Profile for Context

**CRITICAL: Read `PROFILE.md` before beginning any meal planning work.**

Use the Read tool to load `./PROFILE.md`.

From the profile, note:
- Household size and appetite adjustments
- Dietary restrictions (ALWAYS respect these - never suggest restricted items)
- Favorite cuisines and cooking style
- Skill level and available equipment
- Shopping patterns (which stores, how often, delivery options)
- Pantry staples and saved fats
- Typical meal structure (what meals are cooked vs. grabbed)
- Any health goals or current focuses
- Wednesday guests or recurring events
- Standard seasoning blends

This context will inform every decision in the meal planning process.

---

## Step 2: Verify Dates Using System Tools

**CRITICAL: Use Bash date commands to verify all dates. Never rely on LLM date arithmetic.**

Get today's date and calculate the planning period dates:

```bash
# Get today's date
date '+%Y-%m-%d %A'

# For date range calculations, use date arithmetic
# Example: Get date 7 days from now
date -v+7d '+%Y-%m-%d %A'

# Example: Get next Monday
date -v+mon '+%Y-%m-%d %A'
```

Confirm the date range with the user before proceeding.

---

## Step 3: Gather Planning Goals and Constraints

Ask the user about their planning period and goals. Use the AskUserQuestion tool for efficiency when appropriate.

**Essential information:**

1. **Time period:** "What dates are you planning for?" (Default: next 7 days starting tomorrow)
   - Use Bash to verify the dates
   - Confirm: "I understand you're planning from [Day, Date] to [Day, Date]. Is that correct?"

2. **Which meals:** "Which meals do you want to plan?"
   - Options: Dinners only (most common), Dinners + lunches, All meals, Specific days only

**Planning context (gather through conversation):**

3. **Schedule and time constraints:**
   - "Do you have any particularly busy or relaxed days this week?"
   - "Any days where you need quick meals (under 30 min)?"
   - "Any days where you have time for longer/special cooking projects?"

4. **Theme or focus:**
   - "Do you want a theme for this week?"
   - Examples: Asian cuisine, Italian classics, Mediterranean, Comfort food, Light and healthy, Use the freezer, No waste week, Budget week
   - If they mention a theme, ask clarifying questions

5. **Featured dishes:**
   - "Are there 1-2 specific recipes you're excited about making this week that we should build around?"
   - If yes, note these as "anchor recipes" for the plan

6. **Constraints:**
   - "Do you have a budget limit for groceries this week?"
   - "Any health goals to focus on?" (Examples: More vegetables, Less red meat, Lighter meals, Higher protein)

7. **Leftovers and waste:**
   - "Do you have any ingredients you need to use up from the fridge or pantry?"
   - "Any leftover ingredients from last week's plan we should incorporate?"

8. **Social plans:**
   - "Any dinner guests or social meals planned?" (Check if Wednesday guests are happening per profile)
   - "Will you be eating out any nights?"

**Adjust your questions based on their initial answers.** If they give a detailed first response, don't ask redundant questions.

---

## Step 4: Check Recent Meal Plans for Context

Use the Glob tool to find recent meal plan files:

```
Pattern: "meal-plans/*.md"
```

Read the most recent 1-2 meal plans (if they exist) to understand:
- What recipes they've made recently (avoid repetition unless requested)
- What ingredients might still be available (leftover portions, partial packages)
- What worked well or didn't (check feedback sections if present)
- Patterns in their meal planning preferences

This helps avoid suggesting recipes they just made and identifies opportunities to use up ingredients.

---

## Step 5: Build Meal Requirements for Each Day

Based on everything you've learned, create a detailed requirements document for each meal that needs to be planned.

**For each day/meal, document:**

1. **Date and day of week** (verified with Bash)
2. **Meal type** (dinner, lunch, etc.)
3. **Time constraint** (quick/30min, normal/60min, leisurely/90+min, all-day project)
4. **People count** (from profile, adjust for guests)
5. **Cooking context:**
   - Busy day? (German class + wife works late = 15 min max)
   - Relaxed day? (weekend, can do longer projects)
   - Special occasion? (board gaming night, guests)
6. **Cuisine preferences:**
   - From weekly theme (if specified)
   - From profile favorite cuisines
   - Featured dish cuisine (if this is a featured dish day)
7. **Ingredients on hand:**
   - Leftover ingredients from earlier in the week
   - Ingredients user mentioned needing to use up
   - Frozen assets or pantry items to prioritize
8. **Recipe characteristics needed:**
   - Protein type (if specified or to ensure variety)
   - Complexity (staple vs. featured dish)
   - Complete meal vs. needs sides
   - Makes leftovers? (useful for next day)
9. **Constraints:**
   - Dietary restrictions (from profile)
   - Budget considerations
   - Health goals
   - Already used recipes this week (avoid repetition)

**Example requirements document:**

```
Monday, January 5, 2026:
- Meal: Dinner
- Time: Normal (60 min) - first meal after travel, restocking pantry
- People: 2 adults (1.2x servings)
- Context: Just got back from travel, first Rewe shopping trip today
- Cuisine: Comfort food, Italian-American staple preferred
- Ingredients: Restocking trip - use this to anchor week's ingredients
- Recipe needs: Staple recipe, not too complex, complete meal
- Protein: Any (but setting protein variety for rest of week)
- Notes: This recipe should use basic ingredients that can be shared with later meals

Wednesday, January 7, 2026:
- Meal: Dinner
- Time: Featured dish (can prepare all day with slow cooker)
- People: 5-7 (board gaming night)
- Context: FEATURED DISH of the week - impressive but hands-off
- Cuisine: American comfort food
- Ingredients: Use chicken (bones for future stock)
- Recipe needs: Feeds crowd, can be prepped in advance, impressive
- Protein: Chicken (whole chicken preferred)
- Notes: User specifically requested chicken and dumplings, slow cooker variant
```

---

## Step 6: Plan Meals Using suggest-meal Skill

Now use the **suggest-meal** skill for each meal that needs to be planned. Pass all the context you've gathered to minimize what suggest-meal needs to ask.

**For each meal in chronological order:**

1. **Invoke suggest-meal skill** with a detailed prompt containing all requirements:

**Example prompt for suggest-meal:**

"Please suggest a meal for Monday, January 5, 2026 (dinner for 2 adults).

**Context:**
- Just got back from travel, house is empty
- First Rewe shopping trip today - restocking pantry
- Need a comfort food staple, preferably Italian-American
- Time available: Normal (60 min)
- Should use basic ingredients that can be shared with meals later this week
- This is a staple recipe (not the featured dish)

**Constraints:**
- No dietary restrictions
- This week's theme: Ease back into cooking, minimal stress
- This week we're also making: [list any meals already confirmed]

**Ingredients on hand:**
- Just pantry staples (salt, pepper, oil, flour, basic spices)
- Will shop today at Rewe

Please search the recipe collection for appropriate options and present 3-4 suggestions."

2. **Wait for suggest-meal to complete** - it will present options and get user approval

3. **After user approves a meal:**
   - Note the selected recipe and any sides
   - Add to your running meal plan document
   - Update your tracking of:
     - Proteins used (ensure variety)
     - Ingredients that will be available (opened packages, leftovers)
     - Cuisines covered
     - Complexity balance (featured dishes vs. staples)

4. **CRITICAL: Invoke add-to-shopping-list skill** to add ingredients:
   - Pass the recipe and meal date to add-to-shopping-list
   - Let add-to-shopping-list determine appropriate shopping trip
   - Let add-to-shopping-list create or update the shopping list file
   - Track which shopping list files are being created/updated
   - DO NOT present shopping lists to user yet (save for end)
   - DO NOT manually add ingredients to shopping lists yourself
   - **The add-to-shopping-list skill handles ALL shopping list file management**

5. **Update requirements for remaining meals** based on what you've learned:
   - Adjust ingredient availability (now have opened coconut milk, leftover cilantro, etc.)
   - Adjust protein variety (already used chicken, beef, pork)
   - Adjust cuisine variety
   - Adjust complexity balance

6. **Move to next meal** and repeat steps 1-5

**Important notes:**

- **Chronological order:** Always plan meals in chronological order so you can track ingredient usage
- **Context accumulation:** Each meal's context informs the next meal's requirements
- **User approval:** Never add a meal to the plan without user approval from suggest-meal
- **Ingredient tracking:** Keep detailed notes on what ingredients are being used when
- **Shopping list coordination:** Let add-to-shopping-list handle all the shopping trip logic

---

## Step 7: Identify Shopping List Files Created

Before generating the meal plan file, identify all the shopping list files that were created or updated by the add-to-shopping-list skill during this planning session.

**Review what happened:**
1. For each meal you planned, you called add-to-shopping-list
2. Each call to add-to-shopping-list created or updated a shopping list file in `shopping-lists/YYYY-MM-DD.md`
3. Make a list of all the shopping list files involved in this meal plan

**Information to collect for each shopping list:**
- Filename and date (e.g., `shopping-lists/2026-01-05.md`)
- Which store(s) (e.g., "Rewe", "Asian Market")
- Which meals it supports (e.g., "Monday pasta, Wednesday stir-fry")
- Brief summary of items (e.g., "Proteins, fresh produce, dairy")
- Estimated cost (if you can reasonably estimate)

**You will include this information in the meal plan's Shopping Lists section as LINKS to the files, not embedded lists.**

---

## Step 8: Generate Meal Plan File

Once all meals are approved and shopping lists identified, create the comprehensive meal plan file.

**Filename format:** `meal-plans/YYYY-MM-DD to YYYY-MM-DD.md`

Use the Write tool to create the file with this structure:

```markdown
# Meal Plan: [Month Day] to [Month Day, Year]

**Created:** [Today's date]
**Theme/Focus:** [Theme description if applicable]
**Planning Goals:**
- [List 3-5 key goals or focuses for this plan]
- [Examples: "Use frozen assets first", "Featured dish Wednesday", "Keep weeknights under 30 min"]

---

## Plan Overview

[Write 2-3 paragraphs explaining:
- The overall strategy for this week/period
- How meals flow and build on each other
- Key featured dishes or special occasions
- How the plan addresses their stated goals
- Ingredient efficiency approach]

---

## Meal Schedule

### [Day of Week], [Month Day]

**Main:** [Recipe Name](../recipes/recipe-folder/recipe-file.md)

**Sides:**
- [Vegetable side with simple instructions, e.g., "Roasted broccoli (toss with olive oil, salt, pepper; roast 20 min at 220°C)"]
- [Starch side if needed, e.g., "White rice (1 cup rice, 2 cups water, simmer 18 min)"]
- [Or note if meal is complete: "Complete meal - includes vegetables and starch"]

**Why this recipe:** [Explanation of why it fits - schedule, ingredient use, theme, featured dish, etc.]

**Timing:** ~[X] minutes total ([Y] main dish, [Z] sides can cook simultaneously if applicable)

**Notes:**
- [Any prep notes, variations, or special instructions]
- [Connection to other meals - "uses leftover X from Monday"]
- [Side timing notes if relevant - "sides can roast while main simmers"]

---

[Repeat for each meal in the plan]

---

## Ingredient Efficiency & Waste Reduction

[Explain how the plan minimizes waste and uses ingredients efficiently:]

**Key ingredient sharing:**
- [Example: "Coconut milk opened Tuesday used in both Tuesday curry and Thursday soup"]
- [Example: "Cilantro from Monday tacos also used Wednesday and Friday"]
- [Example: "Chicken bones from Saturday roast used for stock on Sunday"]

**Using up ingredients:**
- [List any ingredients from previous week being used up]
- [List any pantry/freezer items being prioritized]

**Minimizing waste:**
- [Strategies used in this plan to reduce waste]
- [Leftover utilization approach]

---

## Shopping Lists

**CRITICAL: DO NOT embed full shopping lists in the meal plan file. Shopping lists are managed separately.**

**Instead, provide a summary with links to the managed shopping list files:**

**Managed shopping lists have been created for each shopping trip. See the shopping-lists folder for detailed, organized lists with checkboxes.**

### Shopping Trips for This Meal Plan

1. **[Day, Month Day, Year]** - [shopping-lists/YYYY-MM-DD.md](../shopping-lists/YYYY-MM-DD.md)
   - Store: [Store name(s)]
   - For: [Which meals this shopping supports]
   - Items: [Brief summary - e.g., "Pre-made salad, olive oil/vinegar"]
   - Estimated cost: [€X-Y]

2. **[Next shopping trip]** - [Link to shopping list file]
   - [Same format as above]

[Repeat for each shopping trip in the plan]

**Total estimated cost for [period]:** €[X-Y]

**Why separate shopping lists:**
- Each shopping list file is managed by the add-to-shopping-list skill
- Shopping lists have smart quantity tracking and allocation
- Users can check off items as they shop
- Multiple meal plans might share shopping trips
- Shopping lists can be updated independently of meal plans

---

## Prep Schedule

[Provide a day-by-day prep guide to make the week easier]

### Weekend Prep (Optional Time-Savers)
- [ ] [Task] - *[brief note about why/benefit]*

### Daily Prep Notes

**[Day of Week]:**
- [ ] [Morning/afternoon prep tasks if applicable]
- [ ] [Shopping trips for this day]
- [ ] [Evening cooking tasks]
- [ ] [Any advance prep for next day]

[Repeat for each day]

### Make-Ahead Opportunities:
- [List recipes/components that can be prepped ahead]
- [Note optimal prep timing]

---

## Notes & Reminders

**Before starting:**
- [ ] [Important checks before week begins]
- [ ] [Inventory to verify]
- [ ] [Advance prep suggestions]

**During the week:**
- [Tips for staying on track]
- [Flexibility notes]
- [Quick swap suggestions if plans change]

**Special considerations:**
- [Any unique aspects of this week's plan]
- [Guest accommodations]
- [Scheduling notes]

---

## Feedback & Adjustments

*(Space for you to add feedback after completing the week)*

**What worked well:**
-

**What didn't work:**
-

**Recipes to make again:**
-

**Recipes to modify or skip next time:**
-

**Leftover ingredients to use next week:**
-

**Notes for future planning:**
-

---

**Generated with meal-planner skill | [Today's date]**
```

---

## Step 8: Consolidate and Present Shopping Lists

Now read all the shopping list files that were created/updated by add-to-shopping-list and present a consolidated view to the user.

**Process:**

1. Use Glob to find all shopping list files
2. Identify which ones were updated during this meal planning session (based on dates)
3. Read each relevant shopping list file
4. Present to user:

**Format:**

"Your meal plan is complete! Here's your shopping schedule:

**Shopping Trip 1: [Day, Date] at [Store(s)]**
- [X] items for [meals]
- See detailed list: [shopping-lists/YYYY-MM-DD.md](shopping-lists/YYYY-MM-DD.md)

**Shopping Trip 2: [Day, Date] at [Store(s)]**
- [Y] items for [meals]
- See detailed list: [shopping-lists/YYYY-MM-DD.md](shopping-lists/YYYY-MM-DD.md)

**Total estimated cost:** [If you can estimate from typical prices]

**Tips:**
- All shopping lists are organized by store section for easy navigation
- Items show which meals they're for
- Quantities are consolidated (no duplicate purchases)
- Unclaimed portions tracked for future use"

---

## Step 9: Present Final Summary

Give the user a complete overview of what was created:

```
✓ Meal plan created: [Month Day] to [Month Day, Year]

**Plan file:** [meal-plans/YYYY-MM-DD to YYYY-MM-DD.md](meal-plans/YYYY-MM-DD to YYYY-MM-DD.md)

**Summary:**
- [X] meals planned ([breakdown by meal type])
- Featured dish: [Recipe name] on [Day]
- Theme: [Theme if applicable]
- Shopping trips: [X] trips ([dates])

**Meal highlights:**
- [Day]: [Recipe] - [brief note]
- [Day]: [Recipe] - [brief note]
- [Day]: [Recipe] - [brief note]

**Ingredient efficiency:**
- [Key sharing example]
- [Waste reduction note]
- [Smart usage note]

**Next steps:**
1. Review the complete meal plan file
2. Check shopping lists before your trips
3. Add any personal notes or modifications
4. Use the prep schedule to stay organized
5. After the week, add feedback to help improve future plans

**Need changes?**
- Swap a specific meal: Use `/suggest-meal` for that date
- Adjust shopping lists: Edit directly or ask me to add/remove items
- Modify prep schedule: Feel free to adjust to your preference

Happy cooking!
```

---

## Important Notes

### Skill Coordination

This skill orchestrates two other skills:

**suggest-meal:**
- Handles recipe discovery and selection for individual meals
- Gets user approval before adding meals
- Integrates with import-recipe and quick-staple as needed
- Returns approved recipe + sides information

**add-to-shopping-list:**
- Handles smart ingredient allocation across shopping trips
- Respects user's shopping patterns from profile
- Tracks quantities and unclaimed portions
- Creates/updates shopping list files

**Your role as meal-planner:**
- Gather overall planning context and goals
- Build detailed requirements for each meal
- Call suggest-meal with rich context to minimize questions
- Call add-to-shopping-list after each approved meal
- Coordinate the overall plan structure
- Generate the final meal plan file
- Present consolidated shopping lists

### Context is Key

The more context you provide to suggest-meal, the better suggestions it can make and the fewer questions it needs to ask. Always include:
- Time constraints
- People count
- Cuisine preferences
- Theme alignment
- Ingredient availability
- Complexity level
- Connection to other meals in the plan

### Chronological Planning

Always plan meals in chronological order because:
- Ingredient availability changes as you plan (opened packages, leftovers)
- Protein and cuisine variety need to be balanced across time
- Shopping trip timing depends on what comes before
- Later meals can use leftovers from earlier meals

### User Approval Flow

The approval flow is:
1. meal-planner gathers overall context
2. meal-planner invokes suggest-meal with rich context
3. suggest-meal presents options and gets user approval
4. User approves a specific meal
5. suggest-meal returns to meal-planner
6. meal-planner invokes add-to-shopping-list
7. add-to-shopping-list updates shopping lists (silently)
8. meal-planner moves to next meal
9. At the end, meal-planner presents all shopping lists together

### Shopping List Presentation

DO NOT present individual shopping lists as you go - this creates noise and confusion. Instead:
- Let add-to-shopping-list work silently in the background
- Track which shopping lists are being updated
- At the end of planning, read and consolidate all updated lists
- Present a clean summary of shopping trips needed

### Error Handling

**If suggest-meal fails or user rejects all options:**
- Ask user what they want to do:
  - Skip this meal
  - Specify a different recipe manually
  - Change the requirements and try again
  - Plan to eat out or order in

**If add-to-shopping-list fails:**
- Note the error
- Continue with planning
- Remind user to manually add ingredients for that meal

**If dates are unclear:**
- Always use Bash to verify dates
- Confirm with user before proceeding

### Flexibility and Iteration

This is a collaborative process:
- If user wants to change direction mid-planning, adapt
- If a meal doesn't fit well, suggest alternatives
- If the plan feels too complex or stressful, simplify
- If user is excited about a recipe, feature it prominently

The goal is a plan that excites them and feels achievable.

---

## Step 10: Complete

The meal planning skill is complete when:
1. All meals are planned and approved
2. Meal plan file is created
3. Shopping lists are all updated
4. User has been given comprehensive summary
5. User knows how to make adjustments if needed

**Integration with other skills:**
- This skill calls: suggest-meal, add-to-shopping-list
- This skill is called by: users directly, no other skills call this
- Users can later adjust individual meals with: suggest-meal
- Users can adjust shopping lists with: add-to-shopping-list or manual edits
