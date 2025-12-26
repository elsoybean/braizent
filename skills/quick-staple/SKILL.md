---
name: quick-staple
description: Capture a familiar staple recipe that you make regularly with minimal planning
---

# Quick Staple Recipe Workflow

This skill helps you document recipes you make regularly - the ones you know by heart, that use mostly on-hand ingredients, and that you can easily modify. These serve as reminders for meal planning and ensure you get needed items on shopping lists.

## Step 1: Read Profile

**FIRST, read the user's PROFILE.md to understand their context.**

Use the Read tool to load `./PROFILE.md`.

From the profile, note:
- Household size and typical serving needs
- Favorite cuisines and cooking style
- Standard seasoning blend (if specified in Cooking Style section)
- Pantry staples (especially saved fats, seasonings, oils)
- Shopping patterns and store preferences
- Any dietary restrictions or accommodations

This information will help you make intelligent assumptions and ask fewer questions.

---

## Step 2: Get Recipe Description

Ask the user to describe their staple recipe in 1-3 sentences.

**Prompt:**
"Describe the recipe you'd like to capture in just a sentence or two. For example:
- 'Pan fried boneless chicken thighs served with dirty white rice quickly fried in the drippings'
- 'Roasted chicken leg quarters rubbed with my usual spice blend over parboiled potatoes and carrots'

What's your recipe?"

Wait for user's description.

---

## Step 3: Ask Clarifying Questions (Profile-Aware)

Now expand on their description with targeted questions. Keep it conversational - they know how to make this, we're just capturing the details.

**IMPORTANT:** Use information from PROFILE.md to make intelligent assumptions and only ask what you need to confirm or clarify.

**Questions to consider (ask only what's needed):**

1. **Recipe name:** "What would you call this dish?" (Suggest a name if obvious from description)

2. **When used:** Make an assumption based on complexity and profile's cooking style. Only ask if unclear. Examples:
   - Simple pan-fry → assume weeknight
   - Long roast → assume weekend or flexible
   - If they mention guests → note for Wednesday guests

3. **Time:** Make an educated guess based on the technique described. Only confirm if uncertain.

4. **Seasoning:**
   - If profile mentions "standard seasoning blend" or "usual spice blend", ASSUME that's what they use unless they specify otherwise
   - If user says "my usual spice blend", "kitchen pepper", "my go-to seasoning", or similar, reference what's in the profile
   - Common names: standard blend, kitchen pepper, Adobo, Sazon, Tony Chachere's, Lawry's, etc.
   - Don't ask about basic seasoning if profile specifies a default blend - just note it in the recipe
   - Only ask about seasoning if they're doing something different from their usual

5. **Main protein preparation:** They described it - just confirm any ambiguity about cooking method

6. **Starch/side:** They described it - capture what they said

7. **Vegetables:** Ask if not mentioned and relevant

8. **Shopping needs:**
   - Check profile for where they get specific items (e.g., Pollofino from Knuspr)
   - Assume pantry staples from profile are on hand
   - Only ask about fresh items they need to buy

9. **Variations:** "What variations do you commonly make?" (Always ask - this is key to flexibility)

10. **Timing notes:** Only ask if protein typically needs defrosting or if there's advance prep

11. **Why it's a go-to:** Ask this - it helps capture the character of the recipe

**Examples of profile-aware assumptions:**

*If profile says "standard seasoning: salt, pepper, onion powder, garlic powder, red pepper flakes":*
- User says "chicken seasoned with my usual blend" → ASSUME that blend, don't ask
- In recipe, write: "Season chicken with standard blend (salt, pepper, onion powder, garlic powder, red pepper flakes)"
- In "Always have on hand" section, list those seasonings

*If profile says user uses "Adobo" or "Tony Chachere's" as standard seasoning:*
- User says "seasoned normally" → ASSUME their standard seasoning
- In recipe, write: "Season with Adobo (user's standard seasoning)"

*If profile says "always saves chicken schmaltz":*
- User mentions "fried in drippings" → Note schmaltz is likely available too

*If profile says "Pollofino from Knuspr":*
- User says "boneless chicken thighs" → ASSUME Pollofino, note it's from Knuspr

*If profile says "2 adults, larger appetites (1.2x)":*
- Set default servings to "2-3" or "Flexible (typically 2-3 with larger portions)"

**Note:** These questions should flow naturally in conversation. Don't make it feel like a form. Skip questions where you can make confident assumptions from the profile.

---

## Step 4: Generate Recipe Name

Create a simple, descriptive name based on their answers.

**Format:** "[Protein], [Preparation Style] with [Key Sides]"

**Examples:**
- "Chicken Thighs, Pan-Fried with Dirty Rice"
- "Chicken Leg Quarters, Roasted with Potatoes and Carrots"
- "Pork Schnitzel with Spaetzle and Mushroom Gravy"
- "Ground Pork-Beef Mix, Bolognese Style with Spaghetti"

**If user provided their own name that's clear and descriptive, use that instead.**

---

## Step 4: Generate Filename

Convert the recipe name to a filename:

1. Convert to lowercase
2. Replace spaces with hyphens
3. Remove commas and special characters
4. Add `.md` extension

**Examples:**
- "Chicken Thighs, Pan-Fried with Dirty Rice" → `chicken-thighs-pan-fried-with-dirty-rice.md`
- "Pork Schnitzel with Spaetzle" → `pork-schnitzel-with-spaetzle.md`

---

## Step 5: Create Recipe Folder and Generate Recipe File

### 5.1 Create the Recipe Folder
Create a folder at `./recipes/[filename-without-extension]/` using the Bash tool:
```bash
mkdir -p recipes/[filename-without-extension]
```

### 5.2 Create the Markdown File
Use the Write tool to create `./recipes/[filename-without-extension]/[filename]` with this structure:

```markdown
# [Recipe Name]

**Type:** Quick Staple
**Typical Meal Slot:** [Weeknight/Weekend/Wednesday guests/Any/Flexible]
**Total Time:** ~[X] minutes
**Servings:** Flexible - adjust as needed (typically [X])

## Description

[1-2 sentence overview of the dish and why it's a staple. Write this based on user's description and "why it's a go-to" answer.]

## Core Components

**Main protein:**
- [Protein with preparation note]
- *Variation notes:* [What can be swapped or changed based on user's variation answers]

**Starch/Side:**
- [Starch/side with preparation note]
- *Variation notes:* [What can be swapped or changed]

[If vegetables are part of the dish:]
**Vegetables:**
- [Vegetables with preparation note]
- *Variation notes:* [What can be swapped or changed]

[If there are sauces, toppings, or other components:]
**Other components:**
- [Component description]

## Shopping Needs

**Usually need to purchase:**
[List items that need to be bought fresh - from user's "shopping needs" answer]

**Always have on hand:**
[List pantry staples used - from user's "shopping needs" answer and pantry staples from PROFILE.md]

**May need depending on variation:**
[List optional items based on variations mentioned]

## Preparation Notes

**Key steps:**
[Write 3-6 HIGH-LEVEL steps based on the recipe description. These should be memory joggers, not detailed instructions. The user knows how to make this.]

**Timing notes:**
[Include defrosting needs, advance prep possibilities, things to watch for - from user's "timing notes" answer]

## Variation Ideas

[List 3-5 variations based on user's answers about variations and flexibility. Format as bullet points with brief descriptions.]

[Always include a note about adapting based on leftovers:]
- **Using leftovers:** [How this can use up ingredients from other meals]

## Meal Planning Notes

*This is a flexible staple recipe. When meal planning:*
[Write 3-4 bullets about:
- When this works well (busy nights, casual dinners, etc.)
- What it pairs well with
- How it can be modified to fit the week's theme
- Any other planning guidance based on user's answers]

## Personal Notes

[Capture the user's answer about "why it's a go-to" and any other personal observations they shared]

## Tags

[quick-staple] [Generate 5-8 additional relevant tags based on:
- Meal timing: weeknight, weekend, quick, under-30-min, under-60-min
- Cuisine: french, italian, german, american, asian, etc.
- Protein: chicken, pork, beef, vegetarian, etc.
- Characteristics: flexible, comfort-food, easy, crowd-pleaser, etc.
- Preparation: pan-fried, roasted, grilled, stir-fry, etc.]
```

**Important formatting notes:**
- Keep instructions high-level and brief
- Emphasize flexibility throughout
- Use the information from PROFILE.md about typical household size, shopping patterns, etc.
- Make variation notes prominent
- Tag with `[quick-staple]` so these are easy to find

---

## Step 6: Confirm Completion

After successfully creating the file, inform the user:

"Successfully captured '[Recipe Name]' as a quick staple recipe!

**Saved to:** [recipes/folder-name/filename.md](recipes/folder-name/filename.md)

**Summary:**
- Main: [protein]
- Side: [starch/side]
- Time: ~[X] minutes
- Perfect for: [when it's typically used]
- Flexibility: [note about variations]

This recipe is tagged with `[quick-staple]` so it's easy to find when meal planning. When you create meal plans, these can be suggested as flexible filler recipes around your featured dishes.

**What would you like to do next?**
- Add another quick staple recipe
- Import a detailed recipe from a URL with /import-recipe
- Update your profile with /build-profile"

---

## Important Notes

**Keep it simple:**
- These recipes should take less than 5 minutes to capture
- Don't ask for precise measurements unless critical
- The goal is documentation, not instruction

**Emphasize flexibility:**
- Variations are expected and encouraged
- These recipes adapt to what's on hand
- They're meant to use up ingredients from other meals

**Distinguish from imported recipes:**
- Imported recipes: detailed, from URLs, exact measurements
- Quick staples: familiar, flexible, memory aids

**Integration with meal planning:**
- Tag consistently so meal planning can identify these
- Note that these are low-stress options
- Highlight how they can adapt to the week's needs

---

## Step 7: Complete

The quick-staple skill is complete. The user now has a documented staple recipe that can be referenced during meal planning.
