---
name: research-recipe
description: Research and develop a personalized version of any recipe from multiple sources
---

# Research Recipe Workflow

This skill helps you research a recipe from multiple perspectives, understand its variations and cultural context, then develop your own personalized version tailored to your taste and needs. This is the premium recipe development experience - think of it as having a professional chef research and adapt a recipe specifically for you.

## Overview

When you give the name of a dish you've seen or eaten, this skill will:
1. Search the web for multiple variations of the recipe
2. Find at least three key versions: simple, authentic, and refined/technical
3. Present an overview of the dish and its variations
4. Work with you to develop YOUR version based on your preferences
5. Save your version in standard format, with research variants preserved for reference

This is a marquee feature - we go all out to make you feel like a professional chef tailoring a recipe.

---

## Step 1: Get Recipe Name and Choose Quality Tier

### 1.1 Check Execution Context

**Check if this skill was invoked from Plan Mode:**

If the user used `/plan` before invoking this skill, they've already selected premium execution mode. In this case:
- Skip the quality tier question (Step 1.2)
- Note that premium routing is active
- Proceed directly to Step 1.3 (get recipe name)

**If invoked directly** (via `/research-recipe` or Skill tool):
- Proceed to Step 1.2 (offer quality tier choice)

### 1.2 Offer Quality Tier Choice (if not already in Plan Mode)

**Prompt:**
"What recipe would you like to research and develop? This could be:
- A dish you ate at a restaurant and want to recreate
- Something you saw on social media or in a video
- A classic dish you want to learn to make properly
- A culturally significant dish you want to understand better

**Research Quality:**

🆓 **Standard** - Good quality research and analysis
- Multiple source perspectives
- Suitable for most recipes
- Uses your configured default models

💎 **Premium** - Highest quality cultural sensitivity and nuanced analysis
- Superior source evaluation and authenticity assessment
- Recommended for: Culturally significant dishes, authentic ethnic cuisine
- Uses your configured premium models
- Cost depends on your routing configuration

Which quality tier would you like?"

Wait for user's response.

**If user chooses Premium:**
- Set `use_premium_routing = true`
- Proceed to Step 1.3

**If user chooses Standard:**
- Set `use_premium_routing = false`
- Proceed to Step 1.3

### 1.3 Get Recipe Name

"What's the name of the dish you'd like to research?"

Wait for user's response.

---

## Step 2: Read Profile for Context

**CRITICAL: Read `PROFILE.md` before beginning research.**

Use the Read tool to load `./PROFILE.md`.

From the profile, note:
- Household size and dietary restrictions
- Favorite cuisines and cooking style
- Skill level and equipment available
- Shopping patterns and pantry staples
- Any cultural connections or preferences

This context will help you tailor the research and final recipe to the user's specific needs.

---

## Step 3: Conduct Multi-Perspective Recipe Research

Now execute the research using the appropriate routing based on user's quality tier choice.

### 3.1 Determine Execution Strategy

**If `use_premium_routing = true` (or in Plan Mode):**

Use Task tool with model hint for premium routing:

```
Task(
  description: "Research recipe with premium cultural sensitivity",
  prompt: "Research [recipe name] from multiple perspectives with highest quality cultural sensitivity.

  Profile context:
  [Include relevant profile information from Step 2]

  Find and analyze AT LEAST three distinct versions:

  A. THE SIMPLE VERSION
  Search: '[recipe name] simple recipe' or '[recipe name] easy recipe'
  Look for: Minimal ingredients, straightforward techniques, accessible to home cooks

  B. THE AUTHENTIC VERSION (CRITICAL PRIORITY)
  Search: '[recipe name] authentic recipe' or '[recipe name] traditional [culture/region] recipe'
  PRIORITIZE: Voices from the culture - first-generation immigrants, cultural food blogs
  Look for: Traditional techniques, cultural significance, family recipes

  C. THE REFINED/TECHNICAL VERSION
  Search: '[recipe name] chef recipe' or '[recipe name] Michelin'
  Look for: Professional chef recipes, advanced techniques, restaurant quality

  For each version found, note:
  - Source URL and author
  - Key techniques and ingredients
  - Cultural context (if applicable)
  - Difficulty level
  - What makes this version unique

  Present comprehensive comparison of all versions found.",
  model: "opus"  # Hint for premium routing
)
```

**If `use_premium_routing = false`:**

Use Task tool without model hint (default routing):

```
Task(
  description: "Research recipe variations from multiple sources",
  prompt: "[Same prompt as above - include all research requirements]"
  # No model hint = uses default routing
)
```

### 3.2 Research Requirements

Regardless of routing, search for multiple versions of the recipe. You need to find AT LEAST three distinct versions:

### A. The Simple Version
Search for: "[recipe name] simple recipe" or "[recipe name] easy recipe"

**What to look for:**
- Minimal ingredients
- Straightforward techniques
- Accessible to home cooks
- Good for weeknight cooking
- Often from food blogs or home cooking sites

### B. The Authentic Version
Search for: "[recipe name] authentic recipe" or "[recipe name] traditional recipe" or "[recipe name] [culture/region] recipe"

**What to look for:**
- Written by members of the culture the dish comes from
- **PRIORITY:** First-generation immigrants sharing family recipes
- Cultural food blogs and community recipe sites
- Traditional techniques and ingredients
- Historical context and cultural significance
- Stories about how the dish is traditionally made and served

**CRITICAL:** For culturally significant dishes, prioritize voices from that culture. A recipe for pho should come from Vietnamese cooks, tacos from Mexican cooks, pasta carbonara from Italian cooks, etc. Look for first-generation immigrants who bridge traditional methods with accessible ingredients.

### C. The Refined/Technical Version
Search for: "[recipe name] chef recipe" or "[recipe name] Michelin" or "[recipe name] gourmet recipe" or "[recipe name] [famous chef name]"

**What to look for:**
- Recipes from professional chefs
- Michelin-starred restaurants (bonus!)
- Advanced techniques (sous vide, specific temperatures, precise timing)
- Restaurant-quality presentation
- Often from culinary publications, chef's books, or high-end food sites
- More complex ingredient lists and preparations

### Additional Searches (If Helpful)
Depending on the dish, you might also search for:
- Regional variations: "[recipe name] [region] style"
- Specific techniques: "[recipe name] [technique]"
- Modern adaptations: "[recipe name] modern recipe"

**Use WebSearch tool multiple times in parallel to gather all versions efficiently.**

---

## Step 4: Fetch Full Recipe Details

For each of the key versions you identified (simple, authentic, refined), use the WebFetch tool to retrieve the complete recipe details.

**WebFetch each URL with the prompt:**
"Extract the complete recipe information including: recipe title, source/author, any cultural or historical context, cuisine type, servings, timing, description, all ingredients with quantities, all instruction steps in order, and any tips or notes about technique or variations."

**Run these WebFetch calls in parallel for efficiency.**

---

## Step 5: Analyze and Synthesize

Now that you have multiple versions, analyze them to understand:

**Key Differences:**
- What ingredients vary between versions?
- Which techniques differ?
- What shortcuts does the simple version take?
- What refinements does the chef version add?
- What cultural context does the authentic version provide?

**Common Ground:**
- What ingredients are essential across all versions?
- What techniques are non-negotiable?
- What's the core identity of the dish?

**Cultural Context:**
- What's the history and significance of this dish?
- How is it traditionally served?
- Are there regional variations?
- What stories or traditions are associated with it?

---

## Step 6: Present Your Research to the User

Now present a comprehensive overview in a professional, engaging way. This should feel like a chef walking you through their research.

**Format your presentation as:**

```markdown
# [Recipe Name] - Recipe Research & Development

I've researched multiple versions of [recipe name] to help you develop your perfect version. Here's what I found:

## About [Recipe Name]

[2-3 paragraphs about the dish: its origins, cultural significance, what makes it special, how it's traditionally enjoyed. Include interesting stories or context from your research.]

## The Versions I Found

### 1. The Simple Version
**Source:** [Name and URL]
**Overview:** [Brief description - what makes this version simple/accessible]
**Key characteristics:**
- [Bullet points about ingredients, techniques, timing]
**Best for:** [When you'd choose this version]

### 2. The Authentic Version
**Source:** [Name and URL - note if author is from the culture]
**Overview:** [Brief description - what makes this version authentic]
**Cultural insights:** [Any stories, traditions, or context shared]
**Key characteristics:**
- [Bullet points about traditional ingredients, techniques, serving]
**Best for:** [When you'd choose this version]

### 3. The Refined Version
**Source:** [Name, any chef credentials, URL]
**Overview:** [Brief description - what makes this version refined]
**Key characteristics:**
- [Bullet points about advanced techniques, special ingredients, presentation]
**Best for:** [When you'd choose this version]

[If you found additional interesting versions, include them too]

## Key Differences Between Versions

**Ingredients:**
[Table or comparison of how ingredients differ]

**Techniques:**
[How the cooking methods differ - simple vs. traditional vs. refined]

**Timing:**
[How long each version takes, active vs. passive time]

## The Essential Elements

Based on all versions, here are the non-negotiable elements that make this dish what it is:
- [Core ingredients that appear in all versions]
- [Essential techniques]
- [The soul of the dish - what you can't compromise on]

## Now Let's Develop YOUR Version

I'd like to tailor this recipe specifically to your preferences, equipment, and cooking style. Let me ask you a few questions:

[Continue to Step 7]
```

---

## Step 7: Collaborate with User to Develop Their Version

Now use the AskUserQuestion tool to understand what the user wants from their version.

**Questions to ask (use AskUserQuestion with 2-4 questions):**

1. **"Which approach resonates most with you?"**
   - Options: Simple/weeknight, Authentic/traditional, Refined/impressive, Balanced blend
   - This helps you understand their primary goal

2. **"What's your timeline for this dish?"**
   - Options: Under 30 min (need shortcuts), 30-60 min (standard), 1-3 hours (special meal), 3+ hours (weekend project)
   - This helps you adjust complexity

3. **"How important is authenticity vs. accessibility?"**
   - Options: Very authentic (will source special ingredients), Mostly authentic (substitute if needed), Accessible (use what I can find easily), Flexible (whatever tastes good)
   - This helps with ingredient choices

4. **"Any specific adaptations needed?"** (if relevant based on profile)
   - Options might include: Vegetarian adaptation, Scale for [X] people, Work with my equipment, Make it less spicy, Make it more substantial, etc.
   - This depends on the specific dish and user's profile

**Adjust your questions based on the specific dish and what you learned from the profile.**

After receiving answers, you might ask follow-up questions if needed to clarify preferences.

---

## Step 8: Develop the User's Personalized Recipe

Based on the user's answers and your research, develop THEIR version of the recipe.

**Your approach:**
1. Start with the version that best matches their goals (simple/authentic/refined)
2. Incorporate elements from the other versions where appropriate
3. Adapt to their skill level, equipment, and available ingredients (from profile)
4. Convert all measurements to metric
5. Adjust serving sizes to their household size (from profile)
6. Add notes about substitutions or variations they might try
7. Include cultural context from the authentic version where relevant
8. Add technical tips from the refined version where they enhance the result

**Write this recipe in a way that:**
- Feels personalized to THEM
- Explains WHY certain steps or ingredients matter
- Gives them confidence they can succeed
- Respects the dish's cultural significance
- Provides context from your research

---

## Step 9: Present the Personalized Recipe for Approval

Show the user your developed version and explain your choices.

**Format:**

```markdown
# Your Personalized [Recipe Name]

Based on your preferences and my research, here's the version I've developed for you:

## My Approach

I've created this version by [explain your strategy - e.g., "starting with the authentic method but adapting timing for a weeknight meal" or "using the refined techniques but with accessible ingredients" etc.].

## Key Decisions I Made:

**From the authentic version:**
- [What you kept and why]

**From the simple version:**
- [What shortcuts or simplifications you incorporated and why]

**From the refined version:**
- [What techniques or refinements you included and why]

**Adapted for you:**
- [Specific changes based on their profile, equipment, preferences]

---

[Full recipe in standard format - use the same template as import-recipe skill]

---

## What do you think?

Does this version feel right for you? Would you like me to adjust anything? For example:
- Make it more/less authentic
- Add/remove complexity
- Adjust timing or technique
- Change any ingredients or quantities
```

Wait for user feedback. Be prepared to iterate and adjust based on their response.

---

## Step 10: Finalize and Save All Versions

Once the user approves their personalized version, save it along with the research variants.

### A. Save the User's Personalized Version

Generate a recipe filename following the standard convention (lowercase, hyphenated, descriptive).

**Example:** `pad-thai` or `chicken-tikka-masala` or `beef-bourguignon`

Create the directory and main recipe file:
```bash
mkdir -p recipes/[recipe-name]
```

Use the Write tool to create `recipes/[recipe-name]/[recipe-name].md` with:
- The user's personalized version
- All the standard sections (Description, Ingredients table, Instructions, Notes, Personal Notes, Tags)
- Metric measurements
- Adjusted for their household size
- Include a special section at the top noting this was developed through research

**Add these sections after the standard metadata:**
```markdown
**Development Notes:** This recipe was developed through research of multiple versions, balancing [simple/authentic/refined - whatever their priorities were] approaches and adapted specifically for your preferences and equipment.

**Research Sources:**
- [Source Name - Simple Version](URL) (Simple version)
- [Source Name - Authentic Version](URL) (Authentic version)
- [Source Name - Refined Version](URL) (Refined version)
- [Any Additional Sources](URL) (Additional research)
```

**IMPORTANT:** Always include the research sources section to give proper credit to the recipe creators whose work informed your research. This is both ethical and useful for the user to explore the original sources.

### B. Save the Research Variants

For each of the key versions you researched (simple, authentic, refined), create variant files in the same directory.

**Filename convention:** `[recipe-name]_[variant-type].md`

Examples:
- `pad-thai_simple.md`
- `pad-thai_authentic.md`
- `pad-thai_refined.md`

Use the Write tool to create each variant file with the format:

```markdown
# [Recipe Name] - [Variant Type] Version

**Variant Type:** [Simple/Authentic/Refined]
**Source:** [Original source name]
**Source URL:** [URL]
**Research Date:** [Today's date]

## About This Version

[Brief explanation of what makes this version special - why it's the simple/authentic/refined version]

[If authentic version, include cultural context, author's background, any stories]

## Original Recipe

[Full recipe as you fetched it, converted to metric and formatted in the standard template]

## Why This Version Matters

[Explain what this version teaches us - what techniques, ingredients, or approaches are noteworthy]

## Comparison to Your Version

[Brief note about how this differs from the user's personalized version and why you made different choices]

---

*This variant is preserved for reference and learning. Your personalized version is in [recipe-name].md*
```

Create all variant files.

---

## Step 11: Confirm Completion

After successfully creating all files, inform the user with an inspiring message:

**Format:**

```markdown
# Recipe Development Complete! 🎉

I've created your personalized version of [Recipe Name] along with the research variants for reference.

## What I've Saved:

**Your Personalized Recipe:**
[recipes/[recipe-name]/[recipe-name].md](recipes/[recipe-name]/[recipe-name].md)

This is YOUR version, tailored to [brief recap of their priorities and adaptations].

**Research Variants (for reference and learning):**
- [recipes/[recipe-name]/[recipe-name]_simple.md](recipes/[recipe-name]/[recipe-name]_simple.md) - The accessible weeknight approach
- [recipes/[recipe-name]/[recipe-name]_authentic.md](recipes/[recipe-name]/[recipe-name]_authentic.md) - Traditional method from [culture/author]
- [recipes/[recipe-name]/[recipe-name]_refined.md](recipes/[recipe-name]/[recipe-name]_refined.md) - Chef-level techniques and refinement

## What Makes Your Version Special:

[2-3 bullet points highlighting what makes their version unique and well-suited to them]

## Next Steps:

- **Try it out!** Your version is ready to cook.
- **Learn more:** Check the variant files to see different approaches and techniques.
- **Experiment:** Use the variants as inspiration for future adaptations.
- **Share feedback:** After you make it, let me know how it went so we can refine it further.

You now have a professionally researched and personalized recipe - enjoy the cooking journey!

---

## Research Credits

This recipe was developed through research of these sources:
- [Source Name](URL) - [Brief description]
- [Source Name](URL) - [Brief description]
- [Additional sources...]

[Add the actual sources you used in your research with their URLs]
```

**CRITICAL:** Always include the research credits at the end of your completion message to properly attribute the recipe creators whose work you researched.

---

## Important Guidelines

### Cultural Sensitivity
- **ALWAYS** prioritize voices from the culture when researching "authentic" versions
- Look for first-generation immigrants sharing family recipes
- Include cultural context and stories when available
- Respect the significance of traditional dishes
- Avoid appropriation - acknowledge origins and give credit
- If the user wants to modify a traditional dish, help them understand what they're changing and why it matters

### Research Quality
- Use WebSearch and WebFetch tools extensively
- Don't settle for the first results - search thoroughly
- Look for diverse sources (blogs, professional sites, cultural publications)
- Verify information across multiple sources
- Include interesting historical or cultural context
- Note when sources have credibility (chef credentials, cultural authority, etc.)
- **ALWAYS preserve source URLs and credits** - include them in the recipe metadata and completion message
- Proper attribution is both ethical and useful for users who want to explore the original sources

### Personalization
- Reference the user's profile throughout
- Explain your decisions - make them feel like part of the process
- Adapt to their skill level without talking down
- Suggest equipment they have, not things they need to buy
- Work with ingredients available in their region
- Respect their time constraints and priorities

### Professional Touch
- Write with confidence and expertise
- Share interesting insights from your research
- Explain WHY certain techniques or ingredients matter
- Make the user feel like they're learning from a professional
- Be encouraging and inspiring
- Celebrate the final result

### Iterative Process
- Be prepared to revise based on user feedback
- Ask clarifying questions when needed
- Offer alternatives and explain trade-offs
- Don't rush - this is a premium experience
- Make adjustments cheerfully and thoroughly

---

## Example Usage Flow

**User:** "I want to research recipe for chicken tikka masala"

**Assistant:** [Step 1 - confirms the recipe]

**Assistant:** [Step 2 - reads profile]

**Assistant:** [Step 3 & 4 - conducts parallel searches and fetches]
- Searches for simple version → finds "Easy Chicken Tikka Masala" from food blog
- Searches for authentic version → finds recipe from Indian food blogger who's a first-gen immigrant
- Searches for refined version → finds recipe from Michelin-starred Indian chef

**Assistant:** [Step 5 - analyzes differences]
- Simple version uses store-bought curry paste
- Authentic version makes spice blend from scratch, shares grandmother's story
- Refined version includes restaurant techniques like tandoor simulation

**Assistant:** [Step 6 - presents comprehensive research with cultural context]

**Assistant:** [Step 7 - asks questions about preferences]
- User wants "mostly authentic but under 60 min"
- User willing to source some special spices but not all
- User cooking for 2 with larger appetites

**Assistant:** [Step 8 - develops personalized version]
- Uses authentic spice technique but pre-toasts and grinds spices
- Includes story from authentic version
- Uses refined version's technique for sauce texture
- Adjusts quantities for 2-3 servings

**Assistant:** [Step 9 - presents for approval and explains choices]

**User:** "Looks great! Maybe add a note about making it ahead?"

**Assistant:** [Revises to add make-ahead notes]

**Assistant:** [Step 10 - saves all versions]

**Assistant:** [Step 11 - celebrates completion with inspiring message]

---

## Skill Complete

The research-recipe skill is designed to be the premium recipe development experience. Take your time, do thorough research, and make the user feel like they're working with a professional chef who's researching and tailoring a recipe specifically for them.
