---
name: quick-meal-pick
description: Quick meal suggestion from local recipes based on simple criteria (fast, cheap alternative to suggest-meal)
---

# Quick Meal Pick Workflow

This is a **streamlined, fast version** of suggest-meal for when you need a quick decision without extensive reasoning. It searches your local recipe collection by tags and suggests standard side dishes using simple pairing rules.

**When to use this:**
- Routine weeknight meals where any appropriate recipe will do
- You're short on time and just need "something to make"
- You trust your recipe collection and don't need web search
- You want minimal questions and fast results

**When to use full suggest-meal instead:**
- Special occasions or featured meals
- You want context-aware suggestions based on recent meals
- You need web search if no local recipes match
- You want creative side dish ideas

---

## Step 1: Quick Context Gathering

Ask the user for basic meal criteria using AskUserQuestion:

**Questions (all at once):**
1. **Time available?** "How much time for cooking?"
   - Options: "Under 30 min", "30-60 min", "1-2 hours", "Flexible"

2. **Cuisine preference?** "Any cuisine preference?"
   - Options: "No preference", "Italian", "Asian", "German", "French", "American", "Mexican"

3. **Protein preference?** "Any protein preference?"
   - Options: "No preference", "Chicken", "Pork", "Beef", "Fish/Seafood", "Vegetarian"

4. **Avoid recent dishes?** "Anything you've made recently to avoid?" (text field)

---

## Step 2: Search Local Recipes

**COST OPTIMIZATION:** This is a straightforward tag search - perfect for fast agents! Consider spawning a task-optimized agent to:
- Parse the search criteria into tag patterns
- Search recipe files using Grep
- Filter results based on constraints
- Pick a random appropriate recipe

Use Grep to search recipes based on the criteria:

### Build Search Pattern

**For time:**
- Under 30 min: `\[quick-staple\]|\[quick\]|\[under-30-min\]`
- 30-60 min: `\[under-60-min\]|\[weeknight\]`
- 1-2 hours: `\[1-2-hours\]|\[weekend\]`
- Flexible: (search all)

**For cuisine** (if specified):
- Look for: `\[italian\]`, `\[asian\]`, `\[chinese\]`, `\[thai\]`, `\[german\]`, etc.

**For protein** (if specified):
- Look for: `\[chicken\]`, `\[pork\]`, `\[beef\]`, `\[fish\]`, `\[vegetarian\]`, etc.

**Combined search:**
```bash
# Example: Quick meal, Italian, Chicken
grep -l -E '\[quick-staple\]|\[under-30-min\]' recipes/**/*.md | xargs grep -l '\[italian\]' | xargs grep -l '\[chicken\]'

# Or use Grep tool with pattern
# Pattern: "(quick-staple|under-30-min).*(italian).*(chicken)"
```

### Filter Results

- Exclude any recipes mentioned in "Avoid recent dishes"
- If multiple matches, pick randomly or by most recent modification (fresher in memory)
- If no matches, relax constraints (remove cuisine/protein, then time)

### If No Local Matches

Tell user: "I didn't find local recipes matching those criteria. Try:
1. Use `/suggest-meal` for web search and recipe import
2. Relax your criteria (I can search with fewer constraints)
3. Use `/quick-staple` to capture a recipe you already know"

Stop here if no local matches.

---

## Step 3: Read Profile for Household Size

**Quickly read PROFILE.md** to get:
- Household size (for serving count)
- Standard side preferences (if mentioned)
- Dietary restrictions (respect these always)

This is a quick read - don't need full context analysis.

---

## Step 4: Read Selected Recipe

Use Read tool to load the chosen recipe file.

Extract:
- Recipe name
- Cuisine type (from tags or name)
- Total time
- Main protein
- Whether it includes starch/vegetables already

---

## Step 5: Suggest Standard Side Dishes

**COST OPTIMIZATION:** This is template-based pairing - perfect for fast agents! Consider spawning a task-optimized agent to:
- Apply the side dish pairing rules below mechanically
- Match cuisine to standard sides using the decision algorithm
- Return 1-2 simple side suggestions using the quick templates

**Use these standardized side pairing rules** based on main dish cuisine:

### Italian Mains
- **IF pasta dish**: Already complete → Serve with crusty bread + simple green salad (olive oil & vinegar)
- **IF protein-focused** (chicken parm, etc.): Pasta (garlic butter/marinara) + roasted vegetables (zucchini, bell peppers, tomatoes)

### Asian Mains (Chinese, Thai, Vietnamese, Japanese)
- **ALWAYS serve with**: Steamed jasmine rice or white rice (jasmine for Chinese/Thai/Vietnamese, short-grain for Japanese)
- **IF stir-fry**: Rice + stir-fried greens (bok choy, Chinese broccoli) OR cucumber salad
- **IF curry**: Rice + simple vegetable (steamed or stir-fried)
- **IF noodle/rice dish**: Already complete (optional: cucumber salad, pickled vegetables)

### German Mains
- **Starch** (pick one): Roasted potatoes (35 min, 220°C), boiled potatoes (20 min), mashed potatoes (25 min), or spaetzle
- **Vegetable** (pick one): Red cabbage (braised or slaw), green beans (steamed/sautéed), roasted carrots (25 min, 200°C)
- **Traditional additions**: Sauerkraut (for pork), pickles/cornichons

### French Mains
- **Starch** (pick one): Roasted fingerling potatoes (30 min, 200°C), rice pilaf (25 min), crusty French bread
- **Vegetable** (pick one): Haricots verts (French green beans, 5 min steam), roasted root vegetables, ratatouille (if summer), simple green salad (vinaigrette)

### American Comfort Food
- **Starch** (pick one): Mashed potatoes (25 min), rice (white/brown, 18-25 min), biscuits/dinner rolls, cornbread (if chili/BBQ)
- **Vegetable** (pick one): Roasted vegetables (broccoli, carrots, Brussels sprouts), steamed green beans (5 min), corn on the cob, coleslaw (for BBQ/fried)

### Mexican Mains
- **IF tacos/enchiladas/burritos**: Usually complete → Mexican rice + refried beans on side
- **IF fajitas**: Serve with warm tortillas + Mexican rice + refried beans + toppings (sour cream, guacamole, salsa, cheese)
- **IF protein-focused**: Mexican rice + refried beans OR black beans + simple salad

### Default (Any Cuisine / Unknown)
- **Starch**: Rice (white/brown, 18-25 min) OR roasted potatoes (35 min, 220°C) OR bread
- **Vegetable**: Roasted seasonal vegetables (20-30 min) OR steamed green vegetables (5-10 min) OR simple green salad (5 min)

### Quick Side Templates

**Roasted vegetables**: "Roasted [vegetable]: Toss with olive oil, salt, pepper; roast [time] at [temp]°C"
- Broccoli: 20 min at 220°C
- Carrots: 25 min at 200°C
- Potatoes: 35 min at 220°C
- Brussels sprouts: 25 min at 220°C

**Steamed vegetables**: "Steam [vegetable] for [time] minutes until tender"
- Broccoli: 5-7 min | Green beans: 5 min | Carrots: 8-10 min

**Rice**: "Cook [type] rice: 1 cup rice + 2 cups water, simmer 18 min"

**Simple salad**: "[Greens] with simple dressing: olive oil, vinegar, salt, pepper"

### Equipment Coordination
- **IF main uses oven**: Suggest oven-roasted sides (cook together)
- **IF main uses stovetop**: Suggest quick stovetop sides OR oven sides
- **IF main is slow-cooker**: Suggest quick sides (15-30 min near serving time)

Apply these rules mechanically based on the main dish cuisine from Step 4.

---

## Step 6: Present Suggestion

Present the meal suggestion to the user:

**Format:**

"🍽️ **Meal Suggestion for [Day]**

**Main:** [Recipe Name]
- Time: [Total Time]
- Servings: [Household size]
- Recipe: [Link to recipe file]

**Sides:**
- [Side 1]: [Quick description or template]
- [Side 2]: [Quick description or template]

**Why this works:** [Cuisine match / Time match / Protein match / etc.]

---

**Next steps:**
1. ✅ **Accept this meal** - I'll show you what to shop for
2. 🔄 **Try again** - I'll pick a different recipe
3. 🔍 **Use suggest-meal instead** - More thorough search with web fallback"

Wait for user's choice.

---

## Step 7: If Accepted - Show Shopping List Prep

If user accepts, offer to add ingredients to shopping list:

"Great! Would you like me to add the ingredients to your shopping list?

I can:
1. Add to existing shopping list (if you have one planned before [date])
2. Create a new shopping list for a trip before [date]
3. Just show you what you need (you'll add manually)"

If they choose option 1 or 2, invoke `/add-to-shopping-list` skill with the recipe.

If they choose option 3, simply list the main ingredients from the recipe file.

---

## Step 8: Complete

The user now has:
- ✅ A quick meal suggestion from their collection
- ✅ Standard side dishes that pair well
- ✅ Option to add to shopping list

**When to recommend full suggest-meal:**
- If user seems dissatisfied with simple suggestions
- If they ask for more creative/context-aware ideas
- If they mention this is a special occasion
- If no local recipes matched their criteria

---

## Cost Comparison

**quick-meal-pick (this skill):**
- Cost: ~$0.10-0.15 per execution (mostly fast model)
- Time: ~30-60 seconds
- Best for: Routine meals, quick decisions

**suggest-meal (full skill):**
- Cost: ~$0.80-1.00 per execution (capable model + reasoning)
- Time: ~2-3 minutes
- Best for: Special meals, creative suggestions, web search needed

---

## Integration Notes

### Called by meal-planner
meal-planner can use quick-meal-pick for routine weeknight days and reserve suggest-meal for featured days.

### User invocation
- `/quick-meal-pick` - Direct invocation
- `/suggest-meal --quick` - Could be an alias

### Fallback to suggest-meal
If quick-meal-pick can't find suitable recipes, recommend user try `/suggest-meal` for more thorough search.

---

## Examples

### Example 1: Quick weeknight meal

**User criteria:**
- Time: 30-60 min
- Cuisine: No preference
- Protein: Chicken
- Avoid: Nothing recent

**Process:**
1. Search for: `[weeknight]` + `[chicken]`
2. Find: chicken-and-dumplings-southern.md
3. Extract: Southern comfort food, 60 min, serves 2
4. Sides: Mashed potatoes (included), add simple green salad
5. Present: "Chicken and Dumplings (Southern comfort food, 60 min)"

**Cost:** ~$0.12

---

### Example 2: Fast Asian meal

**User criteria:**
- Time: Under 30 min
- Cuisine: Asian
- Protein: No preference
- Avoid: Stir-fry (had yesterday)

**Process:**
1. Search for: `[quick-staple]` + `[asian]`
2. Find: fried-rice-quick.md, chicken-stir-fry.md (excluded)
3. Select: fried-rice-quick.md
4. Sides: Already complete (rice dish), add cucumber salad
5. Present: "Quick Fried Rice (15 min, uses leftovers)"

**Cost:** ~$0.10

---

### Example 3: No local matches

**User criteria:**
- Time: Under 30 min
- Cuisine: Mexican
- Protein: Fish

**Process:**
1. Search for: `[quick]` + `[mexican]` + `[fish]`
2. No matches found
3. Tell user: "No local recipes match. Try `/suggest-meal` to search the web for fish taco recipes, or relax your criteria."

**Cost:** ~$0.08 (search only, no suggestion)

---

## Important Notes

### Keep It Simple
This skill is intentionally simple and fast. Don't overthink it - just search tags, pick a match, suggest standard sides.

### Fast Model Usage
Most of this workflow can use fast models:
- Tag searching = mechanical
- Side pairing rules = lookup table
- Template application = mechanical

Only reserve capable models for:
- Reading profile (if complex reasoning needed)
- User communication/decision making

### When to Escalate
Recommend full suggest-meal when:
- ❌ No local recipe matches
- 🎉 User wants something special/creative
- 🌐 User is open to importing new recipes
- 🤔 User asks complex questions about meal pairing

This keeps quick-meal-pick focused on its core purpose: **fast, cheap, simple suggestions from existing recipes**.
