# Model Routing Configuration Guide

This document explains how to set up and use claude-code-router for cost-optimized execution of meal planner skills.

## Quick Start

1. **Install prerequisites:**
   ```bash
   npm install -g @musistudio/claude-code-router
   ```

2. **Install Ollama** (for 100% local execution):
   - Download from https://ollama.com/download
   - Pull required models:
     ```bash
     ollama pull phi3:mini        # 3.8B - fast mechanical tasks
     ollama pull qwen3:8b         # 8B - default operations
     ollama pull qwen2.5:14b      # 14B - long context (optional)
     ```

3. **Get OpenRouter API key** (only needed for premium research):
   - Sign up at https://openrouter.ai
   - Add payment method (only charged when using premium features)
   - Copy your API key

4. **Configure environment:**
   ```bash
   export OPENROUTER_API_KEY="sk-or-v1-YOUR-KEY-HERE"
   ```

5. **Create router config** at `~/.claude-code-router/config.json`:

   **Option A: 100% Local (Recommended for Privacy & Zero Cost)**
   ```json
   {
     "LOG": true,
     "LOG_LEVEL": "info",
     "API_TIMEOUT_MS": 600000,
     "HOST": "127.0.0.1",
     "NON_INTERACTIVE_MODE": false,

     "Providers": [
       {
         "name": "ollama",
         "api_base_url": "http://localhost:11434/v1/chat/completions",
         "api_key": "ollama",
         "models": [
           "phi3:mini",        // 3.8B - mechanical tasks
           "qwen3:8b",         // 8B - default operations
           "qwen2.5:14b"       // 14B - long context
         ],
         "transformer": {
           "use": ["anthropic", {"maxtoken": 16384}]
         }
       },
       {
         "name": "openrouter-paid",
         "api_base_url": "https://openrouter.ai/api/v1/chat/completions",
         "api_key": "${OPENROUTER_API_KEY}",
         "models": [
           "anthropic/claude-sonnet-4",    // Premium research only
           "anthropic/claude-opus-4-5"     // Future use
         ],
         "transformer": {
           "use": ["openrouter"]
         }
       }
     ],

     "Router": {
       "default": "ollama,qwen3:8b",                         // All normal ops run locally
       "background": "ollama,phi3:mini",                     // Mechanical tasks run locally
       "think": "openrouter-paid,anthropic/claude-sonnet-4", // Premium only when chosen
       "longContext": "ollama,qwen2.5:14b"                   // Long context runs locally
     }
   }
   ```

   **Option B: Hybrid with OpenRouter Free Tier (Better for Low-Spec Hardware)**
   ```json
   {
     "LOG": true,
     "LOG_LEVEL": "info",
     "API_TIMEOUT_MS": 600000,
     "HOST": "127.0.0.1",
     "NON_INTERACTIVE_MODE": false,

     "Providers": [
       {
         "name": "ollama",
         "api_base_url": "http://localhost:11434/v1/chat/completions",
         "api_key": "ollama",
         "models": [
           "phi3:mini",        // 3.8B - mechanical tasks only
           "qwen3:8b",         // 8B - fallback if OpenRouter fails
           "qwen2.5:14b"       // 14B - long context
         ],
         "transformer": {
           "use": ["anthropic", {"maxtoken": 16384}]
         }
       },
       {
         "name": "openrouter-free",
         "api_base_url": "https://openrouter.ai/api/v1/chat/completions",
         "api_key": "${OPENROUTER_API_KEY}",
         "models": [
           "deepseek/deepseek-v3:free",              // Default operations (free)
           "meta-llama/llama-3.3-70b-instruct:free"  // Alternative free option
         ],
         "transformer": {
           "use": ["openrouter"]
         }
       },
       {
         "name": "openrouter-paid",
         "api_base_url": "https://openrouter.ai/api/v1/chat/completions",
         "api_key": "${OPENROUTER_API_KEY}",
         "models": [
           "anthropic/claude-sonnet-4",    // Premium research only
           "anthropic/claude-opus-4-5"     // Future use
         ],
         "transformer": {
           "use": ["openrouter"]
         }
       }
     ],

     "Router": {
       "default": "openrouter-free,deepseek/deepseek-v3:free", // Default ops use free tier
       "background": "ollama,phi3:mini",                       // Mechanical tasks still local
       "think": "openrouter-paid,anthropic/claude-sonnet-4",   // Premium when chosen
       "longContext": "ollama,qwen2.5:14b",                    // Long context local
       "fallback": "ollama,qwen3:8b"                           // Falls back to local if internet fails
     }
   }
   ```

### Which Configuration Should You Use?

| Factor | Option A (100% Local) | Option B (Hybrid) |
|--------|----------------------|-------------------|
| **Privacy** | ✅ Complete - nothing leaves your machine | ⚠️ Default ops go to DeepSeek/OpenRouter |
| **Cost** | ✅ $0 for everything except Premium research | ✅ $0 for everything except Premium research |
| **Speed** | ✅ Fast (30-40 tok/s on CPU) | ✅ Similar speed (cloud DeepSeek V3) |
| **Internet Required** | ❌ No (works offline) | ✅ Yes (for default operations) |
| **Hardware Needs** | ⚠️ 8GB RAM minimum for qwen3:8b | ✅ Only need phi3:mini (lighter) |
| **Rate Limits** | ✅ None | ⚠️ 50/day (1,000/day with $10 credits) |
| **Recommended For** | Privacy-conscious, decent hardware | Low RAM, or prefer cloud default ops |

**Most users should choose Option A (100% Local)** for maximum privacy and zero ongoing cost.

**Choose Option B (Hybrid) if:**
- You have limited RAM (< 8GB) and don't want to run qwen3:8b
- You prefer cloud-based models for default operations
- You already use OpenRouter free tier and want consistency

6. **Start the router:**
   ```bash
   ccr start
   ```

7. **Launch Claude Code:**
   ```bash
   ccr code
   ```

## Model Selection Rationale

This configuration uses specific models optimized for different task types:

### phi3:mini (3.8B) - Background Tasks
**Why this model for mechanical tasks:**
- Optimized specifically for instruction-following
- Fastest inference speed (50+ tokens/sec on CPU)
- Lowest memory usage (8GB RAM sufficient)
- Microsoft-tuned for structured tasks
- Perfect for lookup tables and algorithms

**Used for:**
- Unit conversions and measurement lookups
- Store section categorization
- Recipe formatting and tag generation
- HTML template filling
- Package size lookups

### qwen3:8b (8B) - Default Operations
**Why this model for normal operations:**
- Excellent balance of speed and capability
- Superior instruction-following for meal planning tasks
- Strong multilingual support (useful for international recipes)
- Better at structured outputs than Llama 3.1 8B
- Faster than 14B models with sufficient quality for meal planning

**Used for:**
- Meal suggestions and planning
- Profile building conversations
- Recipe research (Standard tier)
- General skill orchestration
- Interactive user dialogs

### qwen2.5:14b (14B) - Long Context
**Why this model for long context:**
- Larger context window (128K tokens)
- Better handling of complex meal plans
- More capable reasoning for edge cases
- Only used when needed (long recipes, large meal plans)

**Used for:**
- Very long recipes (30+ steps)
- Complex meal plans with many recipes
- Large context operations (rarely needed)

### Claude Sonnet 4 - Premium Quality
**Why this model for premium research:**
- Highest quality cultural sensitivity
- Superior source evaluation and authenticity assessment
- Best for nuanced understanding of cuisine traditions
- Only used when user explicitly chooses Premium tier

**Used for:**
- Recipe research (Premium tier only)
- Culturally significant dishes requiring authenticity
- Complex multi-source synthesis with cultural context

### Models NOT Used (and Why)

**qwen3-coder-30B**: Optimized for code generation, not meal planning. MoE architecture (30B total/3B active) provides no advantage over dense 8B for natural language tasks.

**llama3.1:8b**: Good model, but Qwen3 8B has superior instruction-following and structured output capabilities for meal planning workflows.

**OpenRouter free tier**: Keeping everything local provides 100% privacy, no rate limits, works offline, and zero ongoing cost.

## How Routing Works

### Automatic Routing

The router automatically routes requests based on task type:

**Option A (100% Local):**

| Task Type | Route Used | Model | Cost |
|-----------|------------|-------|------|
| Normal operations | `default` | Qwen3 8B (local) | $0 |
| Background tasks | `background` | Phi-3 Mini 3.8B (local) | $0 |
| Plan Mode (`/plan`) | `think` | Claude Sonnet 4 (cloud) | Paid (~$0.30-0.60 per research) |
| Long context (60K+ tokens) | `longContext` | Qwen2.5 14B (local) | $0 |

**Option B (Hybrid):**

| Task Type | Route Used | Model | Cost |
|-----------|------------|-------|------|
| Normal operations | `default` | DeepSeek V3 (cloud, free tier) | $0* |
| Background tasks | `background` | Phi-3 Mini 3.8B (local) | $0 |
| Plan Mode (`/plan`) | `think` | Claude Sonnet 4 (cloud) | Paid (~$0.30-0.60 per research) |
| Long context (60K+ tokens) | `longContext` | Qwen2.5 14B (local) | $0 |
| Fallback (if internet fails) | `fallback` | Qwen3 8B (local) | $0 |

*Subject to rate limits (50 requests/day without credits)

### Skill-Level Routing

Skills use two main routing strategies:

#### 1. Background Execution (Mechanical Tasks)

Mechanical tasks that follow explicit rules use `run_in_background: true`:

```markdown
Task(
  description: "Convert measurements",
  prompt: "[conversion tables + data]",
  run_in_background: true  # Routes to ollama,phi3:mini
)
```

**Skills using background execution (routes to phi3:mini):**
- **import-recipe**: Unit conversions, title formatting, tag generation
- **add-to-shopping-list**: Ingredient filtering, store section mapping, package allocation
- **recipe-card**: HTML generation from template

All background tasks run on your local Phi-3 Mini model (3.8B) for maximum speed and zero cost.

#### 2. Premium Routing (Complex Reasoning)

For premium quality, skills offer user choice:

```markdown
# User chooses Standard or Premium

# If Premium:
Task(
  description: "Research with cultural sensitivity",
  prompt: "[requirements]",
  model: "opus"  # Routes to openrouter-paid,anthropic/claude-sonnet-4
)

# If Standard:
Task(
  description: "Research variations",
  prompt: "[requirements]"
  # No model hint = routes to default (free tier)
)
```

**Skills with quality tiers:**
- **research-recipe**: Offers Standard (free) or Premium (paid) research quality

## Cost Estimates

### With This Configuration (100% Local)

| Skill | Mechanical Tasks | Reasoning Tasks | Total Cost |
|-------|------------------|-----------------|------------|
| **import-recipe** | $0 (phi3:mini) | $0 (qwen3:8b) | **$0** |
| **add-to-shopping-list** | $0 (phi3:mini) | $0 (qwen3:8b) | **$0** |
| **recipe-card** | $0 (phi3:mini) | N/A | **$0** |
| **research-recipe** (Standard) | N/A | $0 (qwen3:8b) | **$0** |
| **research-recipe** (Premium) | N/A | ~$0.30-0.60 (Claude Sonnet 4) | **~$0.30-0.60** |

### Expected Monthly Cost

Typical usage (10 recipe imports, 4 shopping lists, 5 recipe cards, 2 recipe research):
- **With Standard tier research**: $0/month (100% local)
- **With Premium tier research**: $0.60-1.20/month (only when you choose Premium)

**Cost breakdown:**
- 99% of operations: 100% free (runs locally on your machine)
- 1% of operations: Only when you explicitly choose Premium research quality

**Savings vs. Claude direct**: 95-100%

## Using Quality Tiers

### Research Recipe Skill

When you invoke the research-recipe skill, you'll be asked:

```
Which research quality would you like?

🆓 Standard - Good quality research and analysis
- Multiple source perspectives
- Suitable for most recipes
- Uses your configured default models

💎 Premium - Highest quality cultural sensitivity and nuanced analysis
- Superior source evaluation and authenticity assessment
- Recommended for: Culturally significant dishes, authentic ethnic cuisine
- Uses your configured premium models
- Cost depends on your routing configuration

Which quality tier would you like?
```

**When to choose Premium:**
- Culturally significant dishes (pho, tacos, pasta carbonara, etc.)
- When authenticity is critical
- When you want highest quality source evaluation

**When to choose Standard:**
- Most everyday recipes
- Simple dishes or techniques
- Budget-conscious research

### Alternative: Use Plan Mode

You can skip the question by using Plan Mode first:

```bash
/plan
# Then when prompted, say: "Use the research-recipe skill for pad thai"
```

This automatically uses premium routing.

## Troubleshooting

### "Connection refused" from Ollama
```bash
# Verify Ollama is running:
ollama serve
# Or on macOS/Windows, open Ollama app
```

### "Rate limit exceeded" on OpenRouter
- Purchase $10 in credits to unlock 1,000 requests/day
- Or use Ollama models exclusively (100% free)

### Slow local inference
- Enable GPU acceleration (NVIDIA GPUs supported)
- Use smaller models (phi3:mini instead of qwen2.5:14b)
- Increase RAM allocation

### Background tasks not routing to Ollama
- Check router logs: `ccr logs`
- Verify Ollama is running: `ollama list`
- Confirm config file location: `~/.claude-code-router/config.json`

## Advanced Configuration

### Custom Model Providers

You can add additional providers (DeepSeek direct, Gemini, etc.):

```json
{
  "name": "deepseek",
  "api_base_url": "https://api.deepseek.com/chat/completions",
  "api_key": "${DEEPSEEK_API_KEY}",
  "models": ["deepseek-chat"],
  "transformer": {"use": ["deepseek"]}
}
```

### Fallback Configuration

Add fallback routes for reliability:

```json
"Router": {
  "default": "openrouter-free,deepseek/deepseek-v3:free",
  "background": "ollama,phi3:mini",
  "think": "openrouter-paid,anthropic/claude-sonnet-4",
  "fallback": "openrouter-paid,anthropic/claude-haiku-4-5"
}

## Verifying Setup

Test your configuration:

```bash
# 1. Verify Ollama models are available
ollama list
# Should show: phi3:mini, qwen3:8b, qwen2.5:14b, and any others

# 2. Test each model individually
ollama run phi3:mini "Convert 1 cup to ml using standard conversion"
# Expected: Fast response, "240ml"

ollama run qwen3:8b "Suggest a chicken meal for Wednesday dinner"
# Expected: Reasonable meal suggestion

ollama run qwen2.5:14b "This is a test for long context handling"
# Expected: Response confirming 14B model works

# 3. Start router
ccr start

# 4. Launch Claude Code with router
ccr code

# 5. In Claude Code, check configuration
/status

# 6. Test model switching manually
/model ollama,phi3:mini
# Ask: "What is 2 cups in milliliters?"

/model ollama,qwen3:8b
# Ask: "Suggest a meal idea"

# 7. Test a skill with background routing
/import-recipe
# Provide a recipe URL - mechanical tasks should use phi3:mini automatically
```

## Hardware Requirements

### Minimum Configuration
To run the recommended setup (phi3:mini + qwen3:8b):

- **RAM**: 8GB minimum
- **Storage**: 20GB free space
- **CPU**: 4+ cores (Intel/AMD with AVX2 support)
- **GPU**: Optional (runs fine on CPU)

**Performance expectations:**
- phi3:mini: 50+ tokens/sec on CPU
- qwen3:8b: 30-40 tokens/sec on CPU

### Recommended Configuration
For optimal performance (all three models):

- **RAM**: 16GB
- **Storage**: 30GB free space
- **CPU**: 8+ cores
- **GPU**: NVIDIA with 8GB+ VRAM (optional but 5-10x faster)

**Performance with GPU:**
- phi3:mini: 100+ tokens/sec
- qwen3:8b: 80-100 tokens/sec
- qwen2.5:14b: 40-50 tokens/sec

### Model-Specific Requirements

| Model | RAM | Storage | CPU Speed | GPU Speed |
|-------|-----|---------|-----------|-----------|
| phi3:mini (3.8B) | 8GB | 2.2GB | 50+ tok/s | 100+ tok/s |
| qwen3:8b (8B) | 8GB | 4.7GB | 30-40 tok/s | 80-100 tok/s |
| qwen2.5:14b (14B) | 16GB | 8.1GB | 15-20 tok/s | 40-50 tok/s |

**Notes:**
- Speed estimates are for M-series Mac or modern desktop CPUs
- GPU speeds assume NVIDIA RTX 3060+ or similar
- Actual performance varies by hardware configuration

### What If Your Hardware is Limited?

**8GB RAM only:**
- Use phi3:mini + qwen3:8b (recommended config works)
- Skip qwen2.5:14b (you won't need it for most tasks)

**Older/slower CPU:**
- Start with phi3:mini only
- Background tasks will still be fast
- Use OpenRouter free tier for default route instead of qwen3:8b

**Very limited hardware:**
- Use hybrid approach with OpenRouter free tier for default
- Keep phi3:mini local for mechanical tasks
- Still get significant cost savings

## Usage Notes

### Daily Workflow

**With Option A (100% Local):**
```bash
# Start Ollama (if not already running)
# macOS/Windows: Open Ollama app
# Linux: Already running as service

# Start router
ccr start

# Launch Claude Code
ccr code

# Everything runs locally - work offline if you want!
# Only connect to internet when choosing Premium research
```

**With Option B (Hybrid):**
```bash
# Ensure internet connection active

# Start Ollama for mechanical tasks
# macOS/Windows: Open Ollama app
# Linux: Already running as service

# Start router
ccr start

# Launch Claude Code
ccr code

# Default ops use cloud (DeepSeek V3 free tier)
# Mechanical tasks still run locally (phi3:mini)
# Falls back to local if internet fails
```

### When to Use Each Option

**Use Option A (100% Local) when:**
- ✅ You value privacy and want everything local
- ✅ You have 8GB+ RAM
- ✅ You want to work offline
- ✅ You don't want any rate limits
- ✅ You want zero ongoing costs

**Use Option B (Hybrid) when:**
- ✅ You have limited RAM (< 8GB)
- ✅ You prefer cloud-based defaults
- ✅ You're okay with 50-1,000 requests/day
- ✅ You always have internet connectivity
- ✅ You want slightly higher quality defaults (DeepSeek V3 > Qwen3 8B)

### Monitoring Your Usage

**Check OpenRouter usage** (if using Option B or Premium research):
```bash
# Visit https://openrouter.ai/activity
# View your requests and costs
# Free tier shows remaining quota
```

**Check Ollama performance:**
```bash
# See running models
ollama ps

# Check model list
ollama list

# Monitor system resources
# macOS: Activity Monitor
# Linux: htop or top
# Windows: Task Manager
```

## Next Steps

1. **Choose your configuration** (Option A recommended for most users)
2. **Pull the required Ollama models**
3. **Create the router configuration file**
4. **Test each model individually**
5. **Try importing a recipe** to test background routing
6. **Use research-recipe with Standard tier** first
7. **When you need cultural sensitivity**, try Premium tier

## Troubleshooting by Configuration

### Option A (100% Local) Issues

**Problem: Slow inference**
- Check CPU usage - close other apps
- Consider using qwen2.5:14b less often
- GPU acceleration helps significantly (NVIDIA only)

**Problem: High memory usage**
- Don't run qwen3:8b and qwen2.5:14b simultaneously
- Close qwen2.5:14b when not needed: `ollama stop qwen2.5:14b`
- Reduce to just phi3:mini if very constrained

### Option B (Hybrid) Issues

**Problem: Rate limit exceeded**
- Purchase $10 OpenRouter credits (1,000 requests/day)
- Or temporarily switch to Option A config
- Wait 24 hours for rate limit reset

**Problem: Slow cloud responses**
- DeepSeek V3 might be slower during peak hours
- Switch to Option A for better consistency
- Or add fallback: will use local qwen3:8b if slow

**Problem: Internet connectivity issues**
- Fallback route should activate automatically (qwen3:8b)
- Check router logs: router will show fallback usage
- Consider switching to Option A for offline capability

## Summary

**Recommended Setup: Option A (100% Local)**
- 99% of operations: **$0** (runs on your hardware)
- 1% of operations: Only when you choose Premium research (~$0.30-0.60)
- Complete privacy, works offline, no rate limits
- Requires: 8GB RAM, phi3:mini + qwen3:8b + qwen2.5:14b

**Alternative: Option B (Hybrid with OpenRouter Free)**
- 99% of operations: **$0** (DeepSeek V3 free tier + local phi3:mini)
- 1% of operations: Premium research (~$0.30-0.60)
- Good for low-RAM systems, requires internet
- Rate limits: 50/day (1,000/day with $10 credits)

**Both options save 95-100% vs. using Claude Sonnet/Opus directly**

For more details, see:
- [CLAUDE.md](CLAUDE.md) - Complete project instructions and cost optimization strategy
- [README.md](README.md) - Project overview
- [claude-code-router GitHub](https://github.com/musistudio/claude-code-router) - Router documentation
