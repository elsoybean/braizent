---
name: build-profile
description: Interview the user to create or update their meal planning profile with preferences and constraints
---

# Build Profile Workflow

## Step 1: Determine Mode

Check if `PROFILE.md` already exists to determine whether this is a new profile creation or an update.

Use the Bash tool to check: `test -f ./PROFILE.md && echo "exists" || echo "not found"`

**If file doesn't exist (NEW PROFILE MODE):**
Display this message:
"It looks like you don't have a profile yet. Let's build one together! This will take about 10-15 minutes. We'll go through 8 sections:

**Essential (required):**

1. Household & Servings
2. Taste Preferences
3. Dietary Restrictions (critical for safety)

**Important (strongly recommended):** 4. Shopping Schedule 5. Pantry Staples 6. Cooking Style & Constraints

**Optional:** 7. Health Goals 8. Budget Considerations

You can skip sections and come back to them later. Ready to get started?"

Wait for user confirmation before proceeding.

**If file exists (UPDATE PROFILE MODE):**
Use the Read tool to load the existing profile.

Display this message:
"I see you already have a profile! Would you like to:

1. Update a specific section (tell me which one)
2. Review and update the entire profile
3. Add new information to an existing section

What would you like to do?"

If updating specific sections, skip to those sections in the workflow below. Otherwise, continue with full profile creation.

---

## Step 2: Section 1 - Household & Servings (ESSENTIAL)

**Introduction:**
"Let's start with the basics. This helps me scale recipes correctly and ensure you have the right amount of food."

**Questions to ask:**

1. "How many people are you typically cooking for?"

2. "Does this number vary by day of week? For example, just 2 on weekdays but 4 on weekends when the kids visit?"

3. "Are you cooking for any children? If so, what age ranges?"

4. "When you look at a recipe that says 'serves 4', do you find that's about right, or do you prefer larger or smaller portions?"

5. "Do you like having leftovers for lunch the next day, or do you prefer to cook just enough for one meal?"

**Capture:**

- Default household size (number)
- Day-of-week variance (if any)
- Ages (if children)
- Appetite adjustment (standard/larger/smaller - translate to 1x, 1.2x, 0.8x multiplier)
- Leftover preferences

**Confirm:**
Summarize what you captured and ask if it's accurate. Example:
"Got it! So you're cooking for 2 adults on weekdays, 4 people (including 2 kids ages 8-12) on weekends, with standard portions, and you prefer to have some leftovers. Does that sound right?"

---

## Step 3: Section 2 - Taste Preferences (ESSENTIAL)

**Introduction:**
"Now let's talk about what you actually enjoy eating. The meal plans only work if you're excited about the food!"

**Questions to ask:**

1. "What are your favorite cuisines? For example: Italian, Thai, Mexican, Japanese, Mediterranean, Indian, Chinese, French, etc."

2. "What ingredients or foods do you absolutely love? Think about things you'd be happy to eat multiple times a week."

3. "What about foods you dislike or prefer to avoid? (Don't worry about allergies - we'll cover those separately)"

4. "How do you feel about spicy food?"

   - Use AskUserQuestion with options:
     - "Love it - the spicier the better"
     - "Moderate - enjoy some heat but not extreme"
     - "Mild - prefer gentle spices"
     - "Avoid - sensitive to spicy foods"

5. "Do you prefer variety in your meals, or are you happy repeating favorites?"

6. "How adventurous are you with trying new recipes?"
   - Use AskUserQuestion with options:
     - "Love experimenting with new recipes regularly"
     - "Willing to try 1-2 new recipes per month"
     - "Prefer familiar, tested recipes"

**Capture:**

- Favorite cuisines (list)
- Loved ingredients/foods
- Disliked ingredients/foods (note: preference, not allergy)
- Spice tolerance level
- Variety preferences
- Adventurousness level

**Confirm:**
Summarize and verify accuracy.

---

## Step 4: Section 3 - Dietary Restrictions (CRITICAL - ESSENTIAL)

**Introduction (use serious tone):**
"This next section is extremely important for your safety and health. I need to understand any dietary restrictions you have. This includes allergies, intolerances, religious requirements, or ethical choices.

I'll never suggest recipes that violate your restrictions, and I'll never tell you to 'pick out' an ingredient. Your safety is non-negotiable."

**Questions to ask (with extreme care):**

1. "Do you have any food allergies? Please describe them and how severe they are."

   - If they mention anything, ask follow-up: "What happens when you eat [ingredient]? Is this a medical reaction or a strong dislike?"
   - Clarify severity: life-threatening (anaphylaxis), moderate (hives, swelling), or mild (discomfort)

2. "Do you have any food intolerances or sensitivities? For example, lactose intolerance, gluten sensitivity, etc."

   - Ask about what they can tolerate: "Are there any versions of [ingredient] that work for you? For instance, some people with lactose intolerance can handle hard cheeses."

3. "Do you follow any religious dietary laws? Such as kosher, halal, or others?"

4. "Do you follow any dietary patterns by choice? Such as vegetarian, vegan, pescatarian, etc."

   - If vegetarian/vegan, clarify: "Does that include eggs and dairy, or strictly plant-based?"

5. "Are there any cross-contamination concerns I should know about? For example, if a food is processed in a facility with tree nuts."

6. "Is there anything else you absolutely cannot or will not eat that we haven't covered?"

**CRITICAL VALIDATION:**

- For anything that sounds like an allergy, explicitly confirm: "Just to be completely clear - when you say you're allergic to X, is this a medical allergy with physical reactions, or a strong preference to avoid it?"
- Distinguish between:
  - SEVERE ALLERGY (anaphylaxis, life-threatening)
  - ALLERGY (hives, swelling, significant reaction)
  - SENSITIVITY (digestive discomfort, mild reaction)
  - INTOLERANCE (specific issue like lactose)
  - PREFERENCE (dislike, ethical, religious)

**If no restrictions:**
That's perfectly fine. Note that the section will say "None reported" but can be updated anytime.

**Capture:**

- Allergies with severity levels
- Intolerances with details
- Religious restrictions
- Ethical/lifestyle restrictions
- Cross-contamination concerns
- Other absolute avoidances (note if preference vs. medical)

**Confirm:**
Read back EVERY restriction clearly and ask for confirmation. This is critical for safety.

---

## Step 5: Section 4 - Shopping Schedule (IMPORTANT)

**Introduction:**
"Let's talk about how and where you shop. This helps me organize shopping lists in a way that fits your routine."

**Questions to ask:**

1. "What grocery stores do you typically shop at? What's your primary/main store?"

2. "How often do you prefer to grocery shop? Weekly? Twice a week?"

3. "Do you have a regular shopping day? Like Saturday mornings, or flexible?"

4. "Do you shop at bulk stores like Costco, Sam's Club, or BJ's? If so, how often?"

5. "Do you visit any specialty stores? Farmer's markets, Asian markets, Mexican grocers, etc.?"

6. "Are you willing to make multiple shopping trips per week, or do you prefer to get everything in one trip?"

7. "Do you use online grocery delivery or pickup services?"

**Capture:**

- Primary grocery store(s) and frequency
- Regular shopping day (if any)
- Bulk stores and frequency
- Specialty stores and frequency
- Convenience stores (for emergency items)
- Multi-trip willingness
- Online shopping habits

**Confirm:**
Summarize the shopping pattern.

---

## Step 6: Section 5 - Pantry Staples (IMPORTANT)

**Introduction:**
"Let's talk about ingredients you always keep in stock - the things you don't need to add to shopping lists because you always have them. Don't worry about being exhaustive; we can always update this later."

**Questions to ask:**

1. "What basic seasonings and spices do you always have on hand? Think salt, pepper, garlic powder, etc."

2. "Do you have a standard seasoning blend you use for almost everything? For example:"

   - "Some people use salt, pepper, garlic powder, onion powder, and red pepper flakes for most dishes"
   - "Others use 'complete seasonings' like Adobo, Sazon, Tony Chachere's, or 'kitchen pepper' (a pre-mixed blend)"
   - "Or do you season differently for each dish?"

   This is especially important for quick staple recipes - knowing your default seasoning approach helps me write recipes that match how you actually cook.

3. "Do you keep any special umami enhancers on hand? Like MSG, nutritional yeast, fish sauce, etc."

4. "Do you save cooking fats? Some people keep bacon drippings, chicken schmaltz, or duck fat for added flavor."

5. "What cooking oils and vinegars do you keep stocked?"

6. "What about baking essentials? Flour, sugar, baking powder, etc."

7. "What condiments and sauces are always in your pantry or fridge? Like soy sauce, mustard, hot sauce, etc."

8. "What grains, pasta, or rice do you keep regularly?"

9. "Do you keep canned goods or jarred items as staples? Like crushed tomatoes, beans, etc."

10. "Do you keep any stocks or broths on hand?"

**Capture organized by categories:**

- Basics (salt, pepper, oils, saved fats)
- Spices & dried herbs
- Standard seasoning blend (if they have one)
- Umami enhancers (MSG, etc.)
- Condiments & sauces
- Grains, pasta, rice
- Canned & jarred goods
- Baking essentials
- Stocks/broths

**Note to user:**
"This list can start simple and grow over time. I won't add these items to shopping lists, so update this section as you discover patterns in what you always keep stocked."

**Confirm:**
Show the organized list and verify.

---

## Step 7: Section 6 - Health Goals (OPTIONAL)

**Introduction with disclaimer:**
"The next two sections are completely optional. First, health goals.

I want to be clear upfront: I don't provide medical advice. Any health or nutrition goals should be discussed with your healthcare provider. That said, I can help you select meals that align with goals you've set with your doctor or nutritionist.

Would you like to add health goals to your profile, or skip this section?"

**If they choose to skip:**
Note the section as skipped and move to next section.

**If they want to include health goals:**

Ask these questions:

1. "What health or nutrition goals do you have for your meals? For example: more protein, more vegetables, lower sodium, etc."

2. "Are there specific nutrients you're trying to increase or moderate in your diet?"

3. "Do you follow or want to follow any particular dietary pattern? Like Mediterranean, high-protein, etc."

4. "Do you prefer lighter or heartier meals at different times of day?"

**Capture:**

- Stated dietary goals (with user's own words)
- Nutritional targets if specified
- Dietary patterns of interest
- Meal timing preferences

**Confirmation with disclaimer:**
Show what you captured and include this note:
"Remember: This information supports your stated goals. Always consult healthcare providers for medical advice. I will never provide medical recommendations or suggest changing your dietary approach."

---

## Step 8: Section 7 - Cooking Style & Constraints (IMPORTANT)

**Introduction:**
"Let's talk about your cooking style and time constraints. This ensures meal plans are realistic for your life."

**Questions to ask:**

1. "How would you describe your cooking skill level?"

   - Use AskUserQuestion with options:
     - "Beginner - still learning basic techniques"
     - "Intermediate - comfortable with most standard techniques"
     - "Advanced - confident with complex techniques"

2. "How much time do you typically have for cooking on weekdays? Think about active cooking time, not including things baking in the oven."

3. "What about weekends - do you have more time or enjoy longer cooking projects?"

4. "What kitchen equipment do you have? For example:"

   - Slow cooker
   - Instant Pot or pressure cooker
   - Air fryer
   - Food processor
   - Immersion blender
   - Stand mixer
   - Any other special equipment

5. "Are you willing to do meal prep ahead of time? Like spending an hour on Sunday to make the week easier?"

6. "How do you feel about cooking in general?"

   - Use AskUserQuestion with options:
     - "Love it - cooking is my hobby"
     - "Enjoy it - it's relaxing"
     - "It's fine - necessary but not exciting"
     - "It's a chore - prefer quick and efficient"

7. "Are there any cooking techniques you avoid, struggle with, or particularly enjoy?"

**Capture:**

- Skill level
- Weekday time constraints
- Weekend time availability
- Kitchen equipment list
- Meal prep willingness
- Attitude toward cooking
- Technique preferences/avoidances

**Confirm:**
Summarize the cooking profile.

---

## Step 9: Section 8 - Budget Considerations (OPTIONAL)

**Introduction:**
"Last optional section: budget. Understanding your food budget helps me suggest meal plans that are financially comfortable. This is completely optional to share."

**Ask if they want to include budget information:**

**If they skip:**
Note the section as skipped and proceed to profile generation.

**If they want to include:**

Questions to ask:

1. "Do you have a weekly or monthly food budget you try to stay within? Rough range is fine."

2. "Are there ingredients you consider splurge items versus everyday staples?"

3. "Do you prefer budget-friendly recipes most of the time, or are you comfortable with varying costs?"

4. "Do you have any strategies for saving money on groceries? Like buying in bulk, using seasonal produce, etc."

**Capture:**

- Budget range (weekly or monthly)
- Splurge vs. everyday philosophy
- Overall budget approach
- Money-saving strategies

**Confirm:**
Summarize budget preferences.

---

## Step 10: Generate Profile File

Now format all the captured information into the standard `PROFILE.md` structure.

**File location:** `./PROFILE.md`

**Use this template:**

```markdown
# User Profile

_Last updated: [Today's date in YYYY-MM-DD format]_

---

## Household & Servings

[Format the captured information as bullet points]

- Default: [X adults/people]
- [Day variance if applicable]
- [Children info if applicable]
- Appetite: [standard/larger/smaller portions]
- Leftovers: [preference]

---

## Taste Preferences

- **Favorite cuisines:** [comma-separated list]
- **Loves:** [comma-separated list of loved ingredients/foods]
- **Dislikes:** [comma-separated list with note: "taste preferences, not allergies"]
- **Spice tolerance:** [level with description]
- **Variety:** [preference for variety vs. repetition]
- **Adventurousness:** [willingness to try new recipes]

---

## Dietary Restrictions

**⚠️ CRITICAL INFORMATION - Always respect these restrictions absolutely**

[If restrictions exist, organize by category:]

### Allergies

[List each with severity marker:]

- **SEVERE ALLERGY:** [ingredient] - [description of reaction]
- **ALLERGY:** [ingredient] - [description of reaction]
- **SENSITIVITY:** [ingredient] - [description of reaction]

### Intolerances

[List with details about what can/cannot be tolerated]

### Religious/Ethical Restrictions

[List with brief explanation]

### Cross-Contamination

[Note any concerns]

### Other Avoidances

[List preferences that aren't medical - note they are preferences]

[If NO restrictions:]
**No dietary restrictions reported.** This section can be updated anytime if circumstances change.

---

## Shopping Schedule

- **Primary store:** [store name] - [day/frequency]
- **Bulk shopping:** [store name] - [frequency, if applicable]
- **Specialty stores:** [list with frequency, if applicable]
- **Convenience:** [approach to last-minute items]
- **Online:** [usage of delivery/pickup services]
- **Shopping preference:** [one trip vs. multiple trips]

---

## Pantry Staples (Always in Stock)

### Basics

[List basic seasonings, oils, etc.]

### Spices & Dried Herbs

[List]

### Condiments & Sauces

[List]

### Grains & Pasta

[List]

### Canned & Jarred

[List]

### Baking

[List, if applicable]

_Note: This list can be updated as you discover patterns in what you keep stocked._

---

## Health Goals

[If included:]
_⚠️ Disclaimer: This information supports your stated goals. Always consult healthcare providers for medical advice._

- **Goal:** [stated goal]
- **Goal:** [another goal if applicable]
- **Interest:** [dietary patterns]
- **Preference:** [meal timing or other preferences]

[If skipped:]
_This section was not completed. It can be added later if desired._

---

## Cooking Style & Constraints

- **Skill level:** [level] - [brief description]
- **Weekday time:** [constraint]
- **Weekend time:** [availability]
- **Equipment available:**
  - [List equipment with bullet points]
- **Meal prep:** [willingness and approach]
- **Cooking attitude:** [how they feel about cooking]
- **Techniques:** [preferences or avoidances]

[If they have a standard seasoning blend, add this subsection:]

**Standard seasonings & techniques:**

- **Default seasoning blend:** [their standard blend] - used for almost everything unless otherwise specified
- **Umami enhancer:** [MSG, nutritional yeast, etc. if they use one]
- **Saved cooking fats:** [bacon drippings, schmaltz, etc. if they save them]

_When creating quick staple recipes or adapting recipes, assume the standard seasoning blend is used unless a specific seasoning profile is called for._

---

## Budget Considerations

[If included:]

- **Weekly/monthly budget:** [range]
- **Splurge items:** [philosophy]
- **Philosophy:** [overall approach]
- **Strategies:** [money-saving approaches]

[If skipped:]
_This section was not completed. It can be added later if desired._

---

## Learning Notes

_This section is automatically updated based on feedback from completed meal plans._

### Recipes to Repeat

_(Will be populated after using the capture-feedback skill)_

### Recipes to Avoid

_(Will be populated after using the capture-feedback skill)_

### Discovered Preferences

_(Will be populated over time as you provide feedback)_

---

_Profile created: [Today's date in YYYY-MM-DD format]_
_Last modified: [Today's date in YYYY-MM-DD format]_
```

**Implementation:**

- If NEW profile: Use Write tool to create `./PROFILE.md`
- If UPDATE: Use Edit tool to update only the modified sections, then update the "Last modified" timestamp

---

## Step 11: Validate Critical Sections

Before finalizing, validate the profile:

**Check these items:**

✅ **Household & Servings:**

- At least 1 person specified
- Numbers are reasonable (not negative, not absurdly large)

✅ **Dietary Restrictions:**

- If allergies exist, they have severity markers (SEVERE ALLERGY, ALLERGY, SENSITIVITY)
- Clear distinction between medical issues and preferences
- Warning message is present in the section header

✅ **File Format:**

- Valid markdown syntax
- All section headers present (even if sections are empty/skipped)
- Timestamps included
- Proper spacing and readability

**If validation issues are found:**

- Explain the issue to the user
- Ask clarifying questions
- Use Edit tool to fix the issues

---

## Step 12: Confirm Completion

Display a completion message to the user:

"Your profile has been successfully [created/updated] and saved to [PROFILE.md](PROFILE.md)!

**Here's a summary of what I captured:**

- Household: [brief summary]
- Dietary restrictions: [brief summary or "None reported"]
- Favorite cuisines: [list]
- Shopping: [primary store and pattern]
- Cooking style: [skill level and time constraints]
  [Include other notable items]

**You can edit this file anytime** in a text editor if you want to make changes manually. Everything is stored in a simple, readable markdown format.

**What would you like to do next?**

- Import some recipes with /import-recipe
- Update a section of your profile (just tell me which one)
- Ask questions about meal planning

Ready when you are!"

---

## Handling Updates (UPDATE MODE)

When a user wants to update an existing profile:

### For Specific Section Updates:

1. Read the current `PROFILE.md` file
2. Show the user the current content of the section they want to update
3. Ask: "Would you like to replace this entirely, add to it, or modify specific items?"
4. Conduct the interview for that section using the steps above
5. Use the Edit tool to replace just that section
6. Update the "Last modified" timestamp
7. Confirm the changes

### For Full Profile Review:

1. Read the current `PROFILE.md` file
2. Go through each section one by one
3. Show current content and ask: "Does this still look accurate? Want to update anything?"
4. Only re-interview sections that need changes
5. Update modified sections using Edit tool
6. Update the "Last modified" timestamp
7. Provide summary of all changes made

---

## Important Notes

**Privacy:**
If user expresses privacy concerns, reassure them: "All this information stays in a markdown file on your computer. Nothing is sent anywhere. You have complete control and can edit or delete anything at any time."

**Incomplete Interviews:**
If the user needs to stop midway:

- Save all completed sections immediately
- Add a note in incomplete sections: "_Section in progress - will complete later_"
- When they return, read the existing profile and ask which sections to complete

**Medical Advice Boundaries:**
If user asks for medical advice or starts sharing extensive medical details:

- Politely redirect: "I can't provide medical advice. Let's focus on the dietary impact. For medical aspects, please work with your doctor or dietitian."
- Keep the focus on food preferences and restrictions, not medical conditions

**Conflicting Information:**
If user provides contradictory information:

- Point it out gently: "I noticed you mentioned X earlier but just said Y. Which should I note in your profile?"
- Don't assume - always clarify

**Allergy vs. Dislike Clarity:**
Always, always clarify if someone says they're "allergic" to something:

- Ask directly: "When you say allergic, do you mean a medical reaction with physical symptoms, or that you really dislike it?"
- If unclear, err on the side of caution and treat as a restriction

---

## Step 13: Complete

The build-profile skill is now complete. The user has a functional `PROFILE.md` that can be used by other skills like `create-meal-plan` and `capture-feedback`.
