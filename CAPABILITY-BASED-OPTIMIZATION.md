# Capability-Based Cost Optimization

## Philosophy

The Braizent skills use a **capability-based approach** to model selection rather than hardcoding specific model names. This allows the agent system to make intelligent decisions about which models to use based on:

1. **Task complexity** - Mechanical vs. reasoning tasks
2. **Available models** - System can use whatever models are accessible
3. **Future flexibility** - Works with new/better models as they become available
4. **Cost efficiency** - Automatically selects cheapest appropriate model

## Capability Tiers

### Fast/Cheap Models
**Best for:** Mechanical, rule-following tasks
- Lookup table operations (unit conversions, package sizes)
- Pattern matching (title formatting, validation)
- List processing (filtering, categorizing)
- Template filling (markdown generation)
- Simple calculations (scaling, arithmetic)

**Examples:** Haiku, or any fast model the agent has access to

### Capable/Premium Models
**Best for:** Complex reasoning, creativity, judgment
- Cultural sensitivity assessment
- Context-aware suggestions
- Multi-perspective synthesis
- Conversational interviews
- Ambiguity resolution

**Examples:** Sonnet 3.5, Sonnet 4.5, Opus, or any capable model the agent has access to

## Implementation

### Let the System Decide (Preferred)

```markdown
Task(
  description: "Convert recipe measurements",
  prompt: "Use this exact conversion table: [table]

  Convert these ingredients: [list]"
)
```

The agent system sees:
- "exact conversion table" = mechanical task
- Automatically selects fast/cheap model
- Cost: ~70% less than using capable model

### Hint at Capability Level (If Needed)

```markdown
Task(
  description: "Research authentic recipe sources",
  prompt: "Find sources prioritizing voices from the culture...",
  model: "sonnet"  # Hint: this needs cultural sensitivity judgment
)
```

The agent system sees:
- `model: "sonnet"` = capability hint, not specific model
- Selects appropriate capable model (Sonnet 3.5, 4.5, Opus, etc.)
- Gives system flexibility to choose best available model

### Don't Hardcode Versions (Avoid)

```markdown
# ❌ Too rigid - locks to specific model version
Task(
  description: "...",
  model: "claude-sonnet-4-5-20250929"
)

# ✅ Better - capability hint
Task(
  description: "...",
  model: "sonnet"
)

# ✅ Best - let system decide
Task(
  description: "...",
  # no model specified for mechanical tasks
)
```

## Benefits

### 1. Future-Proof
- New models (Haiku 5, Sonnet 6, etc.) automatically used when available
- Don't need to update skills when new models release
- System always uses best available model for the task

### 2. Cost-Efficient
- Fast models used automatically for mechanical tasks
- Capable models reserved for complex reasoning
- 60-80% cost reduction on optimized skills

### 3. Flexible
- Works across different environments (API, CLI, integrations)
- Adapts to user's available models
- No assumptions about specific model availability

### 4. Maintainable
- Skills describe **what needs to be done**, not **which model to use**
- Easier to understand and modify
- Less coupling to infrastructure details

## How Claude Should Interpret This

When Claude sees skill instructions with "COST OPTIMIZATION" annotations:

### Mechanical Tasks (Use Fast Models)
```markdown
**COST OPTIMIZATION:** This is a mechanical task - perfect for fast agents!
```

**Claude should:**
1. Identify this as a rule-following task
2. Spawn agent with Task tool
3. Include complete lookup tables/algorithms in prompt
4. Let agent system pick fast model automatically
5. OR hint with `model: "haiku"` if system doesn't auto-detect

### Complex Tasks (Use Capable Models)
```markdown
**COST OPTIMIZATION:** This requires cultural sensitivity and judgment.
```

**Claude should:**
1. Identify this as a reasoning task
2. Either execute directly OR spawn agent if beneficial
3. If spawning, hint with `model: "sonnet"` to ensure capable model
4. Don't skimp on quality for tasks that need reasoning

### Simple Operations (Use Direct Tools)
```markdown
## Step 1: Read the profile
Use the Read tool to load PROFILE.md
```

**Claude should:**
1. Just use Read tool directly
2. Don't spawn agent for trivial operations
3. Agent overhead not worth it for simple file reads

## Examples

### Example 1: import-recipe (Mechanical Steps)

**Step 3.1-3.3** are mechanical (conversions, formatting, tags):

```markdown
Task(
  description: "Process recipe data with conversions and formatting",
  prompt: "Apply these transformations:

  [Conversion table: 1 cup = 240ml, etc.]
  [Title algorithm: move descriptors after comma]
  [Tag taxonomy: 5-15 tags from these categories...]

  Raw data: [recipe data]

  Return: processed data with metric units, reformatted title, tags"
)
```

System automatically uses fast model. Cost: $0.03 instead of $0.30.

### Example 2: research-recipe (Requires Reasoning)

**Multi-perspective research** needs judgment:

```markdown
Task(
  description: "Research authentic recipe sources",
  prompt: "Find multiple perspectives on this dish:

  1. Simple/accessible versions
  2. Authentic sources (prioritize voices from culture)
  3. Refined/restaurant versions

  Assess cultural authenticity and credibility of sources.",
  model: "sonnet"  # Hint: needs cultural sensitivity
)
```

System uses capable model (Sonnet 3.5/4.5/Opus). Cost: higher, but necessary.

### Example 3: add-to-shopping-list (Mixed)

**Step 3** (filter pantry staples) - mechanical:
```markdown
Task(
  description: "Filter ingredients against pantry list",
  prompt: "Categorize into must_purchase/usually_have/always_have:

  [Profile pantry staples list]
  [Ingredient list]"
)
```
System uses fast model. Cost: $0.02.

**Step 4** (determine shopping trip) - reasoning:
```markdown
# Claude executes directly (needs profile understanding)
```
Uses current capable model. Cost: $0.08.

**Step 6** (smart allocation) - mechanical:
```markdown
Task(
  description: "Execute allocation algorithm",
  prompt: "Apply this algorithm: [algorithm steps]

  [Existing shopping list]
  [New ingredients needed]
  [Package size lookup table]"
)
```
System uses fast model. Cost: $0.02.

Total: $0.12 instead of $0.85 (86% savings).

## Anti-Patterns

### ❌ Don't Hardcode Model Versions
```markdown
# Bad - too specific
model: "claude-haiku-4-5-20251001"
model: "claude-sonnet-4-5-20250929"

# Good - capability hints
model: "haiku"  # if needed
model: "sonnet"  # if needed

# Best - let system decide
# (no model parameter for mechanical tasks)
```

### ❌ Don't Ask User About Models
```markdown
# Bad
"Should I use Haiku or Sonnet for this conversion?"

# Good
[Just spawn agent, system picks appropriate model]
```

### ❌ Don't Waste Capable Models on Mechanical Tasks
```markdown
# Bad
[Use Sonnet to convert 1 cup to ml]

# Good
Task(description: "Convert measurements", prompt: "[table]")
```

### ❌ Don't Spawn Agents for Trivial Operations
```markdown
# Bad
Task(description: "Read profile", prompt: "Read PROFILE.md")

# Good
Read(file_path: "PROFILE.md")
```

## Summary

**Capability-based optimization** means:
- ✅ Describe task complexity, not model names
- ✅ Let agent system select appropriate models
- ✅ Use fast models for mechanical tasks (70-80% savings)
- ✅ Use capable models for reasoning tasks (quality maintained)
- ✅ Future-proof and flexible

Claude should **proactively spawn task-optimized agents** for mechanical steps in optimized skills, trusting the agent system to select the right model tier.
