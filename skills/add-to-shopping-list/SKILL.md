---
name: add-to-shopping-list
description: Add ingredients for a specific meal to a shopping list with smart tracking
---

# Add to Shopping List

This skill adds ingredients needed for a specific meal to the appropriate shopping list, respecting the user's shopping patterns and tracking ingredient quantities to avoid over-purchasing.

## Overview

When you need to add ingredients for a meal to a shopping list, this skill:
1. Reads the user's profile to understand shopping patterns and pantry staples
2. Determines which shopping trip should include these ingredients
3. Tracks quantities purchased vs. quantities claimed by meals
4. Avoids duplicates by claiming from already-planned purchases
5. Organizes by store and department for easy shopping
6. Uses markdown checklists for easy marking off while shopping

## Step 1: Read Profile for Shopping Context

Use the Read tool to load `./PROFILE.md`.

**Extract shopping-related information:**
- Which stores does the user shop at?
- How often do they go to each store?
- When are shopping trips typically planned? (e.g., "Monday evenings at Rewe", "Once a week at Asian market")
- Where do they buy specific items? (e.g., "Pollofino from Knuspr", "Polish sausage from Polish market")
- What are their pantry staples? (items always on hand)
- What are their standard seasonings/cooking staples?

This context determines which shopping trip gets which ingredients.

---

## Step 2: Gather Meal Information

Ask the user what meal they're adding ingredients for:

**Prompt:**
"What meal are you adding to your shopping list?

Please provide:
1. **Date of the meal**: [When will you cook this?]
2. **Recipe name**: [What are you making?]
3. **Ingredients needed**: [List ingredients with quantities, or provide a recipe file path]

Example: 'Wednesday January 8, Chicken and Dumplings, need to add the ingredients from the recipe file'"

**If user provides a recipe file path:**
- Use Read tool to load the recipe
- Extract all ingredients from the ingredient table

**If user lists ingredients directly:**
- Parse the ingredient list they provide

---

## Step 3: Filter Out Pantry Staples

**COST OPTIMIZATION:** This is a mechanical filtering task - perfect for fast agents! Consider spawning a task-optimized agent with the Task tool to:
- Parse the ingredient list
- Compare each ingredient against the profile's pantry staples list
- Categorize into must_purchase / usually_have / always_have lists

Compare the ingredient list against the user's pantry staples from their profile.

**For each ingredient, determine:**
1. **Always on hand** (e.g., salt, pepper, olive oil, flour, sugar)
   - Skip adding to shopping list
   - Track these separately to confirm with user

2. **Usually on hand** (e.g., butter, milk, eggs, onions, garlic)
   - Skip adding to shopping list initially
   - Track these separately to confirm with user

3. **Must purchase** (e.g., specific proteins, fresh vegetables, specialty items)
   - Add to shopping list

**Create three lists:**
- `must_purchase` - definitely need to buy
- `usually_have` - probably on hand, but should confirm
- `always_have` - pantry staples, skip unless user says otherwise

---

## Step 4: Determine Shopping Trip

Based on the meal date and user's shopping patterns, determine which shopping trip should include these ingredients.

**Consider:**
1. **When is the meal?** Need ingredients before then
2. **User's typical shopping schedule** (from profile)
3. **Where to buy each item** (from profile preferences)
4. **Already planned shopping trips** (check existing shopping list files)

**Decision logic:**

*If user has a regular schedule (e.g., "Monday evenings at Rewe"):*
- Choose the last trip before the meal date
- Example: Meal on Wednesday → Monday evening Rewe trip

*If meal requires ingredients from multiple stores:*
- Split ingredients across appropriate stores
- Example: Chicken from Rewe, lemongrass from Asian market

*If no trip is planned before the meal:*
- Create a new shopping trip date
- Suggest to user: "I don't see a shopping trip planned before [meal date]. Should I create a list for [suggested date]?"

**Result:** Map each ingredient to a specific shopping trip (store + date)

---

## Step 5: Check Existing Shopping Lists

Use Glob to find existing shopping list files:
- Pattern: `shopping-lists/*.md`
- Look for files matching the determined shopping trip dates

**For each relevant shopping list file:**
- Use Read tool to load the file
- Parse the structure (stores → departments → items with quantities)
- Build a data structure tracking:
  - What's already being purchased
  - Quantities for each item
  - How much of each item is "unclaimed" (available for meals to use)

**Example tracking structure:**
```
Rice (jasmine, 500g bag):
  - Total purchased: 500g
  - Claimed by Monday's stir-fry: 200g
  - Unclaimed: 300g
```

---

## Step 6: Smart Ingredient Allocation

**COST OPTIMIZATION:** This algorithm-based task is perfect for fast agents! Consider spawning a task-optimized agent with the Task tool to:
- Execute the allocation algorithm below
- Check existing purchases and unclaimed quantities
- Determine package sizes using the lookup tables
- Update tracking notes

For each ingredient in the `must_purchase` list, determine if it should be added or claimed from existing purchases.

**Algorithm:**

For each ingredient needed (e.g., "200g jasmine rice"):

1. **Check if already being purchased on this shopping trip**
   - Search the existing shopping list for this ingredient

2. **If found:**
   - Check unclaimed quantity
   - If unclaimed quantity >= needed quantity:
     - Just claim it (update tracking note)
     - Example: "Rice (500g bag) - *for Monday stir-fry (200g), Wednesday fried rice (200g), 100g remaining*"
   - If unclaimed quantity < needed quantity:
     - Add additional purchase
     - Example: Already buying 500g, need 400g more → add another 500g bag

3. **If not found:**
   - Determine appropriate purchase size
     - Small amounts: buy the smallest practical package
     - Common staples: buy standard size (user will use eventually)
     - Perishables: buy only what's needed for the week
   - Add to shopping list with tracking note
   - Example: "- [ ] Rice, jasmine (500g bag) - *for Wednesday fried rice (200g), 300g remaining*"

4. **Track the claim:**
   - Update internal tracking of what's claimed
   - Include in the item's note in the shopping list

**Package size considerations - Use These Standard Sizes:**

## Standard Package Sizes (Use These Unless User Specifies Otherwise)

### Dairy
- Butter: 250g package (8.8 oz stick equivalent)
- Milk: 1L carton
- Heavy cream: 200ml or 500ml
- Yogurt: 150g individual, 500g tub
- Cheese (block): 200g or 400g
- Cheese (grated): 200g bag

### Pantry Dry Goods
- Flour: 1kg bag (minimum)
- Sugar: 1kg bag
- Rice: 500g, 1kg, or 2kg bag
- Pasta: 500g box
- Dried beans: 500g bag

### Canned Goods
- Tomatoes (crushed/diced): 400g can
- Coconut milk: 400ml can
- Beans: 400g can
- Broth/stock: 500ml or 1L carton

### Fresh Produce (Practical Minimums)
- Onions: Buy by unit (can buy 1-2 onions)
- Garlic: Buy by head (can buy 1 head)
- Fresh herbs: Buy by bunch (cannot buy less than 1 bunch)
- Broccoli: Buy by head or in 500g minimum
- Carrots: 500g bag minimum (or by unit for large carrots)
- Potatoes: 1kg bag minimum (or by unit for large potatoes)
- Leafy greens: Buy by bunch or bag (cannot buy by gram)

### Proteins
- Chicken breasts: Package of 2-4, typically 500g-1kg
- Chicken thighs: Package of 4-6, typically 600g-1kg
- Ground meat: 500g package minimum
- Whole chicken: 1200-1800g typical range
- Fish fillets: Buy by weight, 200g minimum per person typical

### Specialty Items (Note If Larger Package Required)
- If item only comes in large package (e.g., 1kg bag of specialty flour needed for 200g), note: "Buy [package size] - will have [X] remaining"

### Decision Rules
1. IF recipe needs < standard package size: Buy standard package, note remainder
2. IF recipe needs > standard package size: Calculate how many packages needed
3. IF produce can be bought by unit: Specify unit count not weight
4. IF item has short shelf life: Only buy what's needed for the week

---

## Step 7: Determine Store Sections

**COST OPTIMIZATION:** This is pure keyword matching and lookup - ideal for fast agents! Consider spawning a task-optimized agent with the Task tool to:
- Match ingredients against the section mapping below
- Apply the keyword matching algorithm
- Check for profile overrides
- Return section assignments

This straightforward categorization costs ~70% less with a fast model.

For each ingredient being added, determine which store section it belongs to **using this exact mapping:**

## Store Section Assignment (Use This Exact Mapping)

### Produce
**ALL fresh vegetables, fruits, and herbs:**
arugula, basil, bell pepper, broccoli, cabbage, carrot, celery, cilantro, cucumber, garlic, ginger, kale, lemon, lettuce, lime, mushroom, onion, orange, parsley, potato, rosemary, spinach, thyme, tomato, zucchini, apple, avocado, banana, etc.

### Meat & Seafood
**ALL fresh/frozen proteins:**
bacon, beef, chicken, duck, fish, lamb, pork, sausage, seafood, shrimp, turkey, ground meat, steak, chops, etc.

### Dairy & Eggs
**ALL dairy products and eggs:**
butter, cheese (all types), cream, eggs, milk, sour cream, yogurt, cream cheese, cottage cheese, etc.

### Dry Goods & Pantry
**ALL shelf-stable dry goods:**
baking powder, baking soda, beans (dried), breadcrumbs, cereal, cocoa powder, coffee, cornstarch, flour (all types), lentils, nuts, oats, oil (olive, vegetable, etc.), pasta, rice, spices (dried), sugar (all types), tea, vinegar, etc.

### Canned & Jarred
**ALL canned and jarred items:**
beans (canned), broth (canned/boxed), coconut milk, jam, olives, pasta sauce, peanut butter, pickles, salsa, tomatoes (canned), tuna, artichoke hearts, capers, etc.

### Condiments & Sauces
**ALL bottled sauces and condiments:**
fish sauce, honey, hot sauce, ketchup, maple syrup, mayonnaise, mustard, soy sauce, sriracha, worcestershire sauce, BBQ sauce, teriyaki sauce, etc.

### Frozen
**ALL frozen items (except proteins):**
frozen vegetables, frozen fruit, ice cream, frozen pizza, frozen meals, frozen appetizers, etc.

### Bakery / Bread
**ALL fresh baked goods:**
bagels, baguette, bread, croissants, dinner rolls, pita, tortillas, hamburger buns, etc.

### International / Specialty
**ALL ethnic/specialty ingredients not in main sections:**
Asian ingredients (miso, rice vinegar, sesame oil, rice paper, etc.), specialty spices, ethnic ingredients, tahini, etc.

### Beverages
**ALL drinks (if shopping list includes):**
juice, soda, sparkling water, wine, beer, etc.

### Other
**Anything that doesn't fit above categories OR user has specified custom location in profile**

### Override Rule
**IF user's PROFILE.md specifies where they buy something** (e.g., "Pollofino from Knuspr"), **use that instead of standard section**

### Assignment Algorithm
1. Match ingredient name against categories above (keyword matching)
2. IF multiple matches, choose most specific category
3. IF no match, use "Other" section
4. IF profile specifies location/store, honor that first

---

## Step 8: Update or Create Shopping List File

**Determine filename:**
- Format: `shopping-lists/YYYY-MM-DD.md`
- Date is the shopping trip date (not the meal date)

**If file already exists:**
- Use Read tool to load current contents
- Parse structure
- Find the appropriate store section
- Find the appropriate department within that store
- Add new items or update existing items with new claims

**If file doesn't exist:**
- Create new file with standard structure

**Shopping list file structure:**

```markdown
# Shopping List: [Month Day, Year]

**Shopping Date:** [Day of Week], [Month Day, Year]
**Stores:** [List of stores on this trip]
**For Meals:** [List dates/meals this shopping supports]

---

## [Store Name 1] (e.g., Rewe)

### Produce
- [ ] [Item name] ([quantity]) - *for [meal name] ([amount used]), [amount remaining] remaining*
- [ ] [Item name] ([quantity]) - *for [meal 1] ([amount]), [meal 2] ([amount]), [amount remaining] remaining*

### Meat & Seafood
- [ ] [Item name] ([quantity]) - *for [meal name]*

### Dairy & Eggs
- [ ] [Item name] ([quantity]) - *for [meal 1] ([amount]), [meal 2] ([amount])*

### Dry Goods & Pantry
- [ ] [Item name] ([quantity]) - *for [meal name], extra for pantry*

### Bakery / Bread
- [ ] [Item name] ([quantity])

### Frozen
- [ ] [Item name] ([quantity])

---

## [Store Name 2] (e.g., Asian Market)

[Repeat section structure]

---

## Notes

- [Any special shopping notes]
- [Substitution options]
- [Store-specific reminders]

---

**Items assumed on hand** (verify if needed):
- [List of usually_have items not added to list]
- [List of always_have items not added to list]

*If you need any of these items, add them to the appropriate section above.*
```

**Editing approach:**

If updating existing file:
1. Use Edit tool to add new items to appropriate sections
2. Use Edit tool to update existing items with new claims
3. Update "For Meals" list to include new meal
4. Update "Items assumed on hand" section

If creating new file:
1. Use Write tool to create complete file with structure above
2. Include only the stores needed for this shopping trip
3. Organize ingredients into appropriate sections

---

## Step 9: Confirm Pantry Assumptions

Present the list of items assumed to be on hand and ask user to confirm.

**Prompt:**
"I've added [X] ingredients to your shopping list for [date].

**Shopping list updated:** [shopping-lists/YYYY-MM-DD.md](shopping-lists/YYYY-MM-DD.md)

**Items added:**
- [List items added with quantities and which sections]

**Items I'm assuming you already have:**
- [List usually_have items]
- [List always_have items if any are critical to verify]

Do you need any of these items added to the shopping list as well?"

**If user says yes to any items:**
- Add those items to the shopping list
- Use the same smart allocation process

**If user says no / all confirmed:**
- Proceed to completion

---

## Step 10: Provide Summary

Confirm what was done and provide useful context.

**Summary format:**

"✓ Added ingredients for **[Meal Name]** on **[Meal Date]** to shopping list

**Shopping trip:** [Day], [Month Day] at [Store(s)]
**Shopping list:** [shopping-lists/YYYY-MM-DD.md](shopping-lists/YYYY-MM-DD.md)

**What was added:**
- [X] items to [Store 1]
- [Y] items to [Store 2]

**Smart allocation:**
- [N] items claimed from existing purchases (no duplicates!)
- [M] new items added

**Items assumed on hand:** [N] items ([list them briefly])

**Next steps:**
- Review the shopping list before your trip
- Check off items as you shop
- Items are organized by store section for easy navigation

**Need to make changes?**
- You can manually edit the shopping list file
- Or tell me to add/remove items
- Or adjust quantities if needed"

---

## Step 11: Complete

The skill is complete. The user now has:
1. Updated shopping list with new ingredients
2. Smart allocation avoiding over-purchasing
3. Organized by store and section
4. Markdown checklists for easy use while shopping
5. Tracking notes showing what each item is for

**Integration points:**
- **suggest-meal** skill can call this to add meal ingredients to shopping
- **meal-planner** skill can call this to add multiple meals' ingredients
- Users can invoke directly: `/add-to-shopping-list`

---

## Important Notes

### Package Sizes and Practicality

**Be realistic about purchasing:**
- Can't buy "50g flour" - flour comes in 1kg bags minimum
- Can't buy "2 tablespoons butter" - butter comes in 250g packages
- Fresh herbs often come in bunches, not by the gram

**Smart purchasing decisions:**
- Pantry goods: Buy standard package size, track leftovers for future meals
- Fresh produce: Can buy by weight, but note practical minimums (e.g., can't buy half a head of broccoli)
- Proteins: Buy what's available (whole chicken, package of thighs, etc.)

### Tracking Unclaimed Quantities

**Why track unclaimed amounts:**
- Prevents buying duplicate ingredients across multiple meals
- Shows user what they'll have leftover for future use
- Enables smart meal planning (use up that opened coconut milk!)

**Example tracking:**
```
- [ ] Coconut milk (400ml can) - *for Tuesday curry (200ml), Thursday soup (200ml), fully allocated*
- [ ] Jasmine rice (500g bag) - *for Monday stir-fry (200g), 300g remaining for future use*
- [ ] Fresh ginger (200g) - *for Monday stir-fry (30g), Tuesday curry (20g), 150g remaining*
```

### Multi-Store Shopping Trips

**When ingredients come from different stores:**
- Create sections for each store in the same shopping list file
- Note which stores user needs to visit
- Organize visit order based on user's patterns (if known)

**Example:**
```
# Shopping List: January 6, 2026

**Shopping Date:** Monday, January 6, 2026
**Stores:** Rewe (main trip), Asian Market (if time)
**For Meals:** Wednesday curry, Friday stir-fry, Saturday roast

---

## Rewe

[Items available at Rewe]

---

## Asian Market

[Specialty Asian ingredients]

*Note: If you can't make it to the Asian market, substitute [alternatives]*
```

### Date Considerations

**Shopping date vs. meal date:**
- Shopping list is named by SHOPPING DATE (when you shop)
- Meal date is tracked in the notes (what you're shopping for)
- Must shop before the meal date

**Date verification:**
- Use Bash date commands to calculate appropriate shopping dates
- Never guess at dates or use LLM date arithmetic
- Example: `date -v+1d '+%Y-%m-%d'` for tomorrow

### Coordination with Meal Plans

**When adding ingredients from a meal plan:**
- Check if meal plan already has a shopping list section
- Note that meal plans often include consolidated shopping lists
- This skill is for adding individual meals or updating existing lists
- For complete meal plan shopping, the meal-planner skill handles that

### User Control

**Users can always:**
- Manually edit shopping list files (they're just markdown)
- Override your decisions about pantry staples
- Adjust quantities up or down
- Reorganize sections to match their store layout
- Check off items as they shop (markdown checkboxes)

**Respect user preferences:**
- If user says "I'm out of flour", add it even though it's a pantry staple
- If user prefers different section names, adapt
- If user wants more/less detail in notes, adjust

---

## Examples

### Example 1: Adding first meal to new shopping list

**User:** "Add ingredients for Wednesday's chicken and dumplings to my shopping list. The meal is January 8th."

**Process:**
1. Read profile → user shops Monday evenings at Rewe
2. Determine shopping trip → Monday, January 6, 2026
3. Check for existing list → None found
4. Create new shopping list: `shopping-lists/2026-01-06.md`
5. Add ingredients organized by section
6. Filter out pantry staples (flour, salt, pepper assumed on hand)
7. Ask about butter, milk (usually have, confirm)

**Result:** New shopping list created with chicken, vegetables, and confirmed butter/milk.

---

### Example 2: Adding second meal to existing shopping list

**User:** "Add ingredients for Friday's stir-fry to my shopping list. Friday is January 10th."

**Process:**
1. Read profile → user shops Monday evenings at Rewe
2. Determine shopping trip → Monday, January 6, 2026 (same trip as previous meal)
3. Check for existing list → Found `shopping-lists/2026-01-06.md`
4. Load existing list → Already buying jasmine rice (500g), ginger (200g)
5. Smart allocation:
   - Rice: Need 200g, have 300g unclaimed → just claim it
   - Ginger: Need 30g, have 150g unclaimed → just claim it
   - Vegetables: Not on list yet → add them
6. Update existing shopping list with new claims and new items

**Result:** Updated shopping list with minimal new items, smart allocation of existing purchases.

---

### Example 3: Multi-store shopping

**User:** "Add ingredients for authentic pad thai next Tuesday. I need fish sauce, tamarind paste, and rice noodles from the Asian market."

**Process:**
1. Read profile → user goes to Asian market "occasionally when needed"
2. Determine this requires an Asian market trip before Tuesday
3. Check existing shopping lists → Found upcoming Rewe trip Saturday
4. Ask user: "Should I add an Asian market trip for Thursday or Friday, or would you like to go Saturday before your Rewe trip?"
5. User chooses Saturday combined trip
6. Update Saturday shopping list to include both Rewe and Asian Market sections

**Result:** Multi-store shopping list for Saturday with both regular groceries and Asian specialty items.

---

### Example 4: Package size considerations

**User:** "Add ingredients for chocolate chip cookies. I need 200g flour, 100g butter, 150g sugar, 100g chocolate chips."

**Process:**
1. Check pantry staples → User profile says they usually have flour, sugar
2. Ask about flour and sugar → User confirms they have enough
3. Butter → Need 100g, comes in 250g packages
4. Chocolate chips → Need 100g, comes in 200g bags (typical)
5. Add to shopping list:
   - Butter (250g package) - *for cookies (100g), 150g remaining*
   - Chocolate chips (200g bag) - *for cookies (100g), 100g remaining for snacking*

**Result:** Practical package sizes with tracking of leftovers.

---

## Integration with Other Skills

### Called by suggest-meal:
After user approves a meal suggestion, suggest-meal can call this skill to add ingredients to shopping list.

### Called by meal-planner:
Meal-planner creates consolidated shopping lists in meal plan files, but user might want to add individual meals later using this skill.

### Calls other skills:
This skill doesn't typically call other skills, but coordinates with their outputs.

---

## Error Handling

### Shopping date is in the past
"The meal date you specified has already passed, or the logical shopping date would be in the past. Please confirm:
- Is the meal date correct?
- Should I create a shopping list for today or tomorrow instead?"

### No shopping pattern in profile
"I don't see a clear shopping pattern in your profile. When would you like to shop for this meal? The meal is [date], so you'll need to shop before then."

### Store not available
"Your profile indicates you usually buy [item] at [Store], but I don't see [Store] in your regular shopping pattern. Should I:
1. Add it to your [other store] list with a note about substitution
2. Create a special trip to [Store]
3. Suggest an alternative ingredient"

### Can't determine appropriate section
If an ingredient doesn't clearly fit a section, put it in "Other" section with a note asking user to move it if they know where it should go.
