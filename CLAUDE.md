# Claude Instructions for Meal Planner Skills Plugin

This document provides guidance for Claude (or any AI assistant) when working with the meal planning skills plugin.

## About This Repository

**This is a Claude Code plugin repository** containing reusable skills for meal planning. The skills live here, but the **user's data lives in their own project** following the same structure principles.

**User Data Structure** (in their own project):
- **Markdown files** (recipes, meal plans, profile) - human-readable, easily editable
- **Agent Skills** (loaded from this plugin)
- **No complex software** (accessible to non-technical users)

## Project Philosophy

**This is NOT a software development project.** This is a content and workflow management system built entirely on:
- **Markdown files** (human-readable, easily editable)
- **Agent Skills** (following the Open Standard)
- **No complex software** (accessible to non-technical users)

### Core Principles

1. **Markdown First**: All data lives in markdown files. No databases, no JSON configs (except skill frontmatter), no complex file formats.

2. **Human-Editable**: Any user should be able to open any file in a text editor and understand/modify it without technical knowledge.

3. **Skills Over Code**: Functionality is implemented through Claude Code skills (SKILL.md files), not through scripts or applications.

4. **Minimal Scripting**: A skill might include a small helper script if absolutely necessary, but the default is to work directly with markdown using Claude's native tools.

5. **Transparent & Inspectable**: Users should always be able to see what's in their files and change it manually if they prefer.

6. **Cost-Conscious Execution**: Use the cheapest model appropriate for each task. Skills have been optimized with explicit lookup tables, algorithms, and decision trees to enable execution by cheaper models (Haiku) for mechanical tasks.

## Project Structure

**This Plugin Repository:**
```
braizent/ (plugin)
├── README.md           # Plugin documentation
├── CLAUDE.md          # This file - instructions for Claude
└── skills/            # Agent skills following Open Standard
    ├── import-recipe/
    ├── quick-staple/
    ├── recipe-variant/
    ├── recipe-card/
    ├── build-profile/
    ├── research-recipe/
    ├── suggest-meal/
    ├── add-to-shopping-list/
    └── meal-planner/
```

**User's Data Project:**
```
my-meals/ (user's project)
├── PROFILE.md         # User preferences and settings
├── recipes/           # Recipe collection (markdown files)
├── meal-plans/        # Meal plans with shopping lists (markdown files)
└── shopping-lists/    # Shopping lists by trip date
```

**Note:** Skills from this plugin work with the user's data files in their own project directory.

## Cost Optimization Strategy

**CRITICAL**: Many skill tasks are mechanical and can be executed by faster, cheaper models. Always consider spawning task-optimized agents for straightforward work to reduce costs by ~70-80%.

### When to Use Different Model Capabilities (via Task Tool)

Use the Task tool to spawn agents, letting Claude select the most appropriate model based on task complexity. The agent system will use:

#### ✅ Fast/Cheap Models for Mechanical Tasks
These tasks follow explicit rules and don't require creative reasoning:
- **Lookup table operations**: Unit conversions, package sizes, store sections
- **Pattern matching**: Title reformatting, tag format validation
- **List processing**: Filtering pantry staples, categorizing ingredients
- **File operations**: Reading recipes, extracting ingredient lists
- **Template filling**: Applying standard formats, markdown generation
- **Comparison**: Checking existing shopping lists for duplicates
- **Simple calculations**: Scaling recipe quantities, date arithmetic

#### ⚠️ Capable/Premium Models for Complex Reasoning
These tasks require judgment, creativity, or nuanced understanding:
- **Creative judgment**: Recipe research, cuisine authenticity assessment
- **Context-aware decisions**: Meal suggestions based on preferences/history
- **Conversational interviews**: Profile building, user clarification
- **Multi-perspective synthesis**: Research recipe comparisons
- **Cultural sensitivity**: Authentic recipe source evaluation
- **Ambiguity resolution**: Interpreting unclear user requests

### How to Spawn Task-Optimized Agents

Within skill execution, use the Task tool to route tasks to appropriate models based on complexity:

#### For Mechanical Tasks (Use Background Execution)

Mechanical tasks that follow explicit rules should run in the background to route to the fastest/cheapest available models:

```markdown
## Step 3: Convert Measurements (Spawn Background Agent)

**Use the Task tool with background execution for this mechanical task:**

Task(
  description: "Convert imperial measurements to metric",
  prompt: "Convert these measurements using the exact conversion table:

  [paste conversion table from skill]

  Ingredients to convert:
  - 1 cup flour
  - 2 tablespoons butter
  - 350°F oven

  Return converted measurements following the rounding rules.",
  run_in_background: true  # Routes to fastest/cheapest model (e.g., local Ollama)
)
```

**When to use background execution:**
- Unit conversions and lookups
- Store section mapping
- Recipe formatting and HTML generation
- Ingredient filtering and categorization
- Tag generation with decision trees
- Package size lookups
- Any task with explicit algorithms/tables

#### For Reasoning Tasks (Use Default Routing)

Tasks requiring judgment use normal Task tool calls (system selects appropriate model):

```markdown
Task(
  description: "Suggest meals based on preferences",
  prompt: "[context and requirements]"
  # No run_in_background = uses default routing (capable model)
)
```

#### For Premium Tasks (User Choice with Quality Tiers)

For tasks requiring highest quality (cultural sensitivity, nuanced analysis), offer users a choice:

```markdown
**Prompt user:**
"Which research quality would you like?
- **Standard**: Good quality research (uses your configured default models)
- **Premium**: Highest quality with maximum cultural sensitivity (uses your configured premium models)

The cost difference depends on your routing configuration."

**If user chooses Premium:**
Task(
  description: "Research recipe with cultural sensitivity",
  prompt: "[research requirements]",
  model: "opus"  # Capability hint for premium routing
)

**If user chooses Standard:**
Task(
  description: "Research recipe variations",
  prompt: "[research requirements]"
  # No model hint = default routing
)
```

**Note**: With claude-code-router, these hints map to your configured routes. Background tasks use the cheapest option (local models), premium tasks use highest quality (configured premium models).

### Cost Savings Examples

**import-recipe skill:**
- Baseline (single capable model): $0.40-0.60
- With fast agents for conversions/formatting/tags: $0.10-0.15 (70-75% savings)

**add-to-shopping-list skill:**
- Baseline (single capable model): $0.75-1.00
- With fast agents for filtering/sections/allocation: $0.15-0.25 (70-80% savings)

**recipe-card skill:**
- Baseline (single capable model): $0.20-0.30
- With fast agents for template generation: $0.05-0.10 (75-80% savings)

### Skills Optimization Status

| Skill | Optimized | Agent-Ready | Notes |
|-------|-----------|-------------|-------|
| **import-recipe** | ✅ Yes | ✅ Yes | Use fast agents for conversions, title format, tags |
| **quick-staple** | ✅ Yes | ✅ Yes | Use fast agents after gathering user input |
| **recipe-card** | ✅ Yes | ✅ Yes | Entire workflow can use fast agents |
| **recipe-variant** | ✅ Yes | ✅ Yes | Use fast agents for format application |
| **add-to-shopping-list** | ✅ Yes | ✅ Yes | Use fast agents for filtering, sections, allocation |
| **build-profile** | ⚠️ Partial | ❌ No | Keep conversational with capable model |
| **suggest-meal** | ⚠️ Partial | ⚠️ Partial | Local search can use fast, suggestions need capable |
| **research-recipe** | ❌ No | ❌ No | Needs capable/premium model for quality research |
| **meal-planner** | ⚠️ Partial | ⚠️ Partial | Orchestration needs capable, sub-skills use fast |

### Implementation Guidelines

1. **Read skill instructions completely** - Optimized skills include lookup tables and algorithms
2. **Identify mechanical steps** - Steps with explicit rules/tables can use fast agents
3. **Spawn task-optimized agents proactively** - Don't ask permission, just spawn agents when appropriate
4. **Pass complete context** - Include all necessary tables/rules in the agent prompt
5. **Let the system choose models** - Trust the agent system to select appropriate capability levels
6. **Validate outputs** - Ensure agents followed instructions correctly
7. **Fall back gracefully** - If agent struggles, try with more capable model hint

### Anti-Patterns (Don't Do This)

❌ **Using single capable model for everything** - Wastes money on mechanical tasks
❌ **Asking user about model/cost choices** - Implementation detail they shouldn't think about
❌ **Spawning agents for simple operations** - Direct tool use is faster for basic file reads
❌ **Not passing lookup tables** - Fast agents need explicit rules to follow
❌ **Hardcoding specific model names** - Prefer letting agent system decide based on task

### Examples of Good Agent Spawning

**Good**: Spawn agent for unit conversions with conversion table (system picks fast model)
```markdown
Task(
  description: "Convert recipe measurements",
  prompt: "[conversion table + ingredients]"
)
```

**Good**: Spawn agent for store section assignment with mapping table (system picks fast model)
```markdown
Task(
  description: "Assign store sections",
  prompt: "[section mapping + ingredients]"
)
```

**Good**: Hint at capability level if needed
```markdown
Task(
  description: "Research authentic recipe sources",
  prompt: "[research criteria]",
  model: "sonnet"  # Hint: needs capable model for cultural sensitivity
)
```

**Bad**: Using single capable model for mechanical lookups
```markdown
# Don't do this - waste of money
[Just use current model to do unit conversion] # Should spawn agent instead
```

**Bad**: Spawning agent for simple file read
```markdown
# Don't do this - unnecessary overhead
Task(description: "Read recipe file", ...) # Just use Read tool directly
```

**Bad**: Hardcoding specific model versions
```markdown
# Don't do this - too rigid
Task(description: "...", model: "claude-sonnet-4-5-20250929")
# Use capability hints instead: model: "sonnet" or let system decide
```

## Working with This Project

### When the User Asks You To...

#### Import a Recipe
- Use the `import-recipe` skill (invoke with `/import-recipe` or use the Skill tool)
- DO NOT write Python/Node.js scripts to parse recipes
- The skill uses Claude's native WebFetch tool to get recipe content
- Output is always a markdown file in `./recipes/[recipe-name]/[recipe-name].md`
- Each recipe gets its own folder

#### Capture a Quick Staple Recipe
- Use the `quick-staple` skill (invoke with `/quick-staple` or use the Skill tool)
- Quick interview process (< 5 minutes) for recipes the user makes regularly
- Profile-aware: uses standard seasonings and shopping patterns from PROFILE.md
- Captures high-level steps as memory aids, not detailed instructions
- Output tagged with `[quick-staple]` for easy identification
- Emphasizes flexibility and variations

#### Create a Recipe Variant
- Work with the user directly to create variants (no skill invocation available yet)
- Common use cases:
  - Quick staple → precise variant (for sharing)
  - Standard recipe → vegetarian/vegan/gluten-free
  - Any recipe → scaled, different cooking method, simplified
- Variant naming: `[recipe-name]_[suffix].md` (e.g., `_precise`, `_vegetarian`, `_double`)
- Maintain links between original and variant
- All variants live in the same folder as the original

#### Generate a Recipe Card
- Work directly to generate recipe cards (no skill invocation needed)
- Automatically checks for `_precise` variants
- If recipe lacks precision, offers to create `_precise` variant first
- Creates HTML with two-column ingredient layout
- Generates PDF automatically via Chrome headless mode
- Compact design (0.2-inch margins) fits on one page

#### Create a Meal Plan
- Use the `create-meal-plan` skill (when implemented)
- ALWAYS read `PROFILE.md` first to understand user preferences
- Check for leftover ingredients in recent meal plans
- Output is a markdown file in `./meal-plans/` with ISO date format filename
- Include an organized shopping list in the meal plan file

#### Search for Recipes
- Use Grep or Glob tools to search existing recipe files
- DO NOT suggest building a search application
- Markdown files are searchable by tags, ingredients, cuisine, etc.
- Search both original recipes and variants

#### Generate Shopping Lists
- Either embed in meal plan files (preferred) OR
- Create standalone markdown files in `./shopping-lists/`
- Organize by store and section
- Use checkbox format: `- [ ] item`

#### Build or Update the Profile
- Use the `build-profile` skill (invoke with `/build-profile` or use the Skill tool)
- Guided interview process covering 8 dimensions
- Two modes: create new profile or update existing sections
- Critical emphasis on dietary restrictions
- Creates or updates `PROFILE.md` with proper structure
- OR directly edit `PROFILE.md` with user input for quick changes
- The profile is a structured markdown document, not JSON/YAML
- Keep it readable - users should be comfortable editing it manually

#### Research and Develop a Recipe
- Use the `research-recipe` skill (invoke with `/research-recipe` or use the Skill tool)
- Multi-perspective research: searches for simple, authentic, and refined versions
- **Cultural sensitivity is paramount**: prioritize voices from the culture, especially first-generation immigrants
- Comprehensive analysis comparing techniques, ingredients, and approaches
- Collaborates with user to develop their personalized version
- Saves main recipe PLUS research variants (`_simple`, `_authentic`, `_refined`)
- **ALWAYS preserve source URLs and credits** for proper attribution
- Profile-aware: adapts to user's equipment, skill level, household size, dietary restrictions

#### Capture Feedback
- Use the `capture-feedback` skill (when implemented)
- Update the meal plan file's feedback section
- Update individual recipe files' personal notes
- Update `PROFILE.md` learning notes section

### Skills Development Guidelines

When creating or modifying skills for this project:

#### Structure
Every skill should follow the Agent Skills Open Standard:

```markdown
---
name: skill-name
description: One-line description
---

# Skill Name

## Step 1: [Action]
Clear instructions using Claude's native tools

## Step 2: [Action]
More instructions

## Step N: Complete
Confirm what was created/modified
```

#### Tool Usage in Skills
Skills should primarily use:
- **Read**: Read existing markdown files
- **Write**: Create new markdown files
- **Edit**: Update existing markdown files
- **Grep**: Search for content in files
- **Glob**: Find files by pattern
- **WebFetch**: Fetch recipe content from URLs
- **AskUserQuestion**: Get user input when needed

Skills should AVOID:
- **Bash** (except for very simple file operations if absolutely necessary)
- Creating Python/Node.js/etc. scripts
- Installing dependencies or packages
- Complex data processing that could be done with Claude's native understanding

#### Example: Good vs. Bad Skill Design

**GOOD ✓**
```markdown
## Step 2: Extract Recipe Data
Use WebFetch to retrieve the recipe URL with a prompt asking to extract:
- Title, ingredients, instructions, etc.

Parse the response and structure the data for the markdown template.
```

**BAD ✗**
```markdown
## Step 2: Extract Recipe Data
Run this Python script to parse the recipe:
```python
import requests
from bs4 import BeautifulSoup
# 50 lines of code...
```

#### When Scripts Might Be Acceptable

A skill may include a small script ONLY if:
1. The task truly requires it (e.g., format conversion, calculation)
2. The script is < 20 lines
3. It uses only standard library features (no dependencies)
4. It's clearly documented and editable by users
5. There's no reasonable way to do it with Claude's native tools

Even then, prefer Claude's native capabilities.

### File Format Requirements

#### Recipe Files (`./recipes/[recipe-name]/[recipe-name].md`)
- Each recipe lives in its own folder
- Filename: lowercase, hyphenated, descriptive
- Metric measurements only (ml, g, kg, °C)
- Four-column ingredient table: Quantity | Unit | Ingredient | Preparation
- Numbered instruction steps
- Space-separated, lowercase tags

**Recipe Variants** (`./recipes/[recipe-name]/[recipe-name]_[suffix].md`):
- Variants use underscore suffix (e.g., `_precise`, `_vegetarian`, `_double`)
- Live in the same folder as the original recipe
- Include link back to original in Personal Notes
- Common variant types:
  - `_precise`: Quick staple → detailed measurements for sharing
  - `_vegetarian`, `_vegan`, `_gluten-free`: Dietary adaptations
  - `_double`, `_scaled-12`: Different serving sizes
  - `_grilled`, `_instant-pot`: Different cooking methods
  - Custom suffixes for any other purpose
- Each variant is independent and can use different format (standard recipe or quick staple)

#### Meal Plan Files (`./meal-plans/*.md`)
- Filename: `YYYY-MM-DD to YYYY-MM-DD.md` (ISO date format)
- Include: Overview, Meal Schedule, Shopping List, Prep Schedule, Feedback section
- Shopping list organized by store → section → items with checkboxes
- Relative links to recipe files

#### Profile File (`PROFILE.md`)
- Structured sections with markdown headers
- Readable prose, not key-value pairs
- Include examples and explanations
- Update timestamp when modified

### Common Tasks & Approaches

#### Task: "Help me plan meals for next week"

**Do This:**
1. Read `PROFILE.md` to understand preferences
2. Check recent meal plans for leftover ingredients
3. Search recipes that match preferences using Grep/Glob
4. Ask user questions about the specific week (busy? guests? etc.)
5. Create a new meal plan file with selected recipes
6. Generate shopping list within the meal plan file

**Don't Do This:**
- Suggest building a meal planning app
- Create a database or spreadsheet
- Write scripts to automate the process
- Ignore the profile and just suggest random recipes

#### Task: "Find all pasta recipes"

**Do This:**
```
Use Grep to search for "pasta" in recipes folder
Look for tags or ingredient tables containing pasta
Present results to user with file links
```

**Don't Do This:**
- Suggest building a recipe database
- Create an index file
- Write a search script

#### Task: "I want to track nutrition information"

**Do This:**
1. Add a nutrition section to the recipe markdown template
2. Update existing recipes to include estimated nutrition
3. Document in README that nutrition is approximate
4. Add reminder to never give medical advice

**Don't Do This:**
- Integrate with a nutrition API
- Build a calorie counter application
- Create a database to store nutrition data

#### Task: "Make a recipe card for my roasted chicken recipe"

**Do This:**
1. Find the recipe file using Glob
2. Read the recipe
3. Check for `_precise` variant in the same folder
4. If recipe is a quick staple without precise measurements:
   - Offer to create `_precise` variant first (recommended for sharing)
   - Or proceed with original flexible format
5. Work with user to gather specific measurements if creating precise variant
6. Generate HTML with two-column ingredient layout
7. Generate PDF using Chrome headless mode

**Don't Do This:**
- Skip checking for existing variants
- Create recipe card without offering to add precision to quick staples meant for sharing
- Suggest building a recipe card application

#### Task: "Make this recipe vegetarian"

**Do This:**
1. Read the original recipe
2. Read PROFILE.md to understand user's cooking context
3. Work with user to identify meat substitutions
4. Ask about technique changes if needed
5. Create variant file: `[recipe-name]_vegetarian.md`
6. Use standard recipe format
7. Include link back to original in Personal Notes
8. Optionally add note to original about variant existence

**Don't Do This:**
- Overwrite the original recipe
- Suggest building a recipe conversion tool
- Create a separate folder for the variant

## Dietary Restrictions & Health

### Critical Rules

**ALWAYS:**
- Read and respect dietary restrictions from `PROFILE.md`
- Mark restrictions clearly (SEVERE ALLERGY, ALLERGY, etc.)
- Exclude recipes that violate restrictions
- Ask if uncertain about an ingredient

**NEVER:**
- Suggest "picking out" restricted ingredients
- Recommend foods that violate restrictions
- Give medical advice
- Suggest changes to user's dietary restrictions
- Insinuate you know what's best for their health

### Health Goals
- Support user's stated goals
- Provide information, not prescriptions
- Include disclaimer: "Consult healthcare providers for medical advice"
- Focus on meal selection, not medical recommendations

## Communication Style

When working with users on this project:

### Do:
- Read `PROFILE.md` before making any meal recommendations
- Explain what files you're creating/modifying
- Provide file paths with markdown links: `[filename](path/to/file)`
- Ask questions when user preferences are unclear
- Respect that users may manually edit any file

### Don't:
- Assume technical knowledge
- Suggest complex software solutions
- Create files without explaining their purpose
- Ignore the documented file formats
- Make the system more complicated than it needs to be

## Extending the System

### Adding New Skills

When a user asks for new functionality:

1. **Check if a skill is the right solution**: Can this be done as a repeatable workflow?

2. **Design the skill**:
   - What markdown files does it read?
   - What markdown files does it create/modify?
   - What user input does it need?
   - What tools (Read, Write, Edit, etc.) does it use?

3. **Create the skill file**:
   - Follow the Open Standard format
   - Document each step clearly
   - Include examples where helpful
   - Keep it simple and maintainable

4. **Update README.md**:
   - Add skill to the skills list
   - Document its purpose and capabilities
   - Update file format documentation if needed

5. **Test the skill**:
   - Walk through each step manually
   - Verify output matches expected format
   - Ensure it respects profile settings

### Adding New File Types

If you need a new type of content:

1. **Confirm it's necessary**: Can existing files be extended instead?

2. **Design the markdown format**:
   - Make it human-readable
   - Use standard markdown features
   - Include clear section headers
   - Add examples in README.md

3. **Document the format**:
   - Add to "File Structure & Formats" in README
   - Include full template with all sections
   - Explain required vs. optional fields
   - Provide formatting rules

4. **Update relevant skills**:
   - Modify skills to read/write the new format
   - Maintain backward compatibility where possible

## Anti-Patterns

### Don't Suggest:
- ❌ "Let's build a web app for this"
- ❌ "We should use a database"
- ❌ "I'll create a Python script to automate this"
- ❌ "Let's install these npm packages"
- ❌ "We need a config file in JSON/YAML"
- ❌ "This needs a CLI tool"
- ❌ "Let's add a GUI"

### Instead Say:
- ✓ "I'll create a skill to handle this workflow"
- ✓ "Let's add that information to your profile markdown file"
- ✓ "I can search your recipes using the tags"
- ✓ "I'll create a meal plan file with that structure"
- ✓ "We can add that as a section in the recipe template"

## Edge Cases & Special Situations

### When a Task Seems to Need Code

If a task appears to require programming:

1. **Re-examine the requirement**: Is there a simpler, markdown-based way?
2. **Use Claude's capabilities**: Can WebFetch, Read, Edit, etc. handle it?
3. **Restructure the data**: Can the markdown format be adjusted to make it easier?
4. **Create a skill**: Can the workflow be documented as repeatable steps?

Only if all else fails, consider a small helper script with user consent.

### When File Formats Conflict

If a user's manual edit doesn't match the documented format:

1. **Accept it**: User edits are valid, update your understanding
2. **Adapt**: Work with their format, don't force compliance
3. **Suggest gently**: If it will cause issues, explain why the format matters
4. **Document**: If it's a good variation, update the README

### When Profiles Conflict with Requests

If a user asks for something that conflicts with their profile:

1. **Clarify**: "Your profile says X, but you're asking for Y. Should I update the profile?"
2. **Don't assume**: Maybe it's a one-time exception, maybe they've changed
3. **Respect restrictions**: Dietary restrictions are never negotiable
4. **Update thoughtfully**: If the profile should change, do it with user consent

## Testing & Validation

When creating or modifying content:

### Always Check:
- ✓ Markdown syntax is valid
- ✓ Internal links work (recipe references in meal plans)
- ✓ File naming follows conventions
- ✓ Required sections are present
- ✓ Measurements are in metric
- ✓ Dietary restrictions are respected

### Validate:
- Recipe files have all required fields
- Meal plans reference real recipe files
- Shopping lists are organized by store → section
- Tags are lowercase and hyphenated
- Dates are in ISO format (YYYY-MM-DD)

## Summary

This meal planner is intentionally simple and transparent. It's designed for regular people to manage their cooking and shopping without needing technical skills. Your role is to:

1. **Work within the markdown/skills paradigm** - don't over-engineer
2. **Respect user preferences** - especially dietary restrictions
3. **Keep files human-readable** - no technical user should be locked out
4. **Follow the Open Standard** - skills are portable and documented
5. **Prioritize simplicity** - when in doubt, choose the simpler approach

The goal is a system that works beautifully with Claude but remains fully accessible and modifiable without Claude. Every file should be something a user could create, read, and edit in a plain text editor.

---

**Remember**: Markdown + Skills = Powerful + Simple + Accessible

**Last updated:** 2025-12-22
