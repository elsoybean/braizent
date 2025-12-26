# Skill Optimization Test Harness

This test harness validates cost optimization strategies by running the same skill inputs through different models (Sonnet 4.5, Sonnet 3.5, Haiku) and comparing:
- Token usage (input + output)
- Cost per execution
- Quality/accuracy of results
- Execution time

## Structure

```
test-harness/
├── README.md                 # This file
├── test-cases/              # Input test cases
│   ├── import-recipe.json
│   ├── add-to-shopping-list.json
│   ├── suggest-meal.json
│   ├── research-recipe.json
│   └── quick-staple.json
├── baselines/               # Sonnet 4.5 baseline outputs
│   ├── import-recipe/
│   ├── add-to-shopping-list/
│   └── ...
├── results/                 # Test run results
│   ├── sonnet-3.5/
│   ├── haiku/
│   └── comparison-reports/
└── scripts/                 # Test execution scripts
    ├── run-test.sh
    ├── compare-outputs.py
    └── generate-report.py
```

## Test Cases

### Phase 1: Mechanical Skills (Haiku target)

1. **import-recipe** (Test Case 1)
   - Input: URL to Italian Osso Buco recipe
   - Validations:
     - Unit conversions (400°F → 200°C)
     - Title formatting (Osso Buco, Italian)
     - Tag generation
   - Target: Haiku ≥90% quality vs. Sonnet 4.5

2. **add-to-shopping-list** (Test Case 2)
   - Input: Chicken-and-dumplings ingredients for Monday Knuspr
   - Validations:
     - Pollofino from Knuspr (not Rewe)
     - Package sizes (flour 1kg not 200g)
     - Store sections
     - Smart allocation
     - Pantry staple filtering
   - Target: Haiku ≥90% quality vs. Sonnet 4.5

3. **recipe-card**
   - Input: Existing recipe markdown
   - Validations:
     - HTML formatting
     - Ingredient table structure
     - Print-friendly layout
   - Target: Haiku ≥90% quality vs. Sonnet 4.5

### Phase 2: Smart Skills (Multi-tier target)

4. **suggest-meal** (Test Case 3)
   - Quick mode (Haiku): Tag-based search, template sides
   - Smart mode (Sonnet 3.5): Context-aware, creative
   - Validations:
     - Recipe selection appropriateness
     - Side dish pairing
     - Profile adherence
   - Target: Quick ≥90%, Smart ≥95% quality vs. Sonnet 4.5

5. **research-recipe** (Test Case 4)
   - Quick mode (Sonnet 3.5): Single search, brief comparison
   - Deep mode (Sonnet 4.5/Opus): Multi-perspective, cultural sensitivity
   - Validations:
     - Recipe quality/sources
     - Cultural context (deep mode)
     - Adaptation to profile
   - Target: Quick ≥95%, Deep 100% quality

6. **quick-staple** (Test Case 5)
   - Optimized (Haiku): Batched questions, template filling
   - Validations:
     - Profile awareness
     - Flexibility capture
     - Template structure
   - Target: Haiku ≥90% quality vs. Sonnet 4.5

## Running Tests

### 1. Generate Baselines (Sonnet 4.5)

```bash
cd test-harness
./scripts/run-test.sh --skill import-recipe --model sonnet-4.5 --baseline
```

This will:
- Read test case from `test-cases/import-recipe.json`
- Execute skill with Sonnet 4.5
- Save output to `baselines/import-recipe/output.json`
- Log token usage, cost, time

### 2. Run Optimization Test (Haiku/Sonnet 3.5)

```bash
./scripts/run-test.sh --skill import-recipe --model haiku --compare
```

This will:
- Execute same test case with Haiku
- Save output to `results/haiku/import-recipe/output.json`
- Log metrics
- Generate diff vs. baseline

### 3. Compare & Report

```bash
./scripts/compare-outputs.py --skill import-recipe
```

Generates comparison report:
- Token usage comparison
- Cost comparison
- Quality assessment (automated + manual checklist)
- Side-by-side output diff

### 4. Full Suite

```bash
./scripts/run-test.sh --all --models sonnet-3.5,haiku
```

Runs all test cases through all specified models and generates comprehensive report.

## Metrics Tracked

### Automated Metrics
- **Input tokens**: Skill instructions + context
- **Output tokens**: Generated content
- **Total tokens**: Input + output
- **Cost**: Based on model pricing
- **Execution time**: Seconds
- **Cost savings %**: vs. Sonnet 4.5 baseline

### Quality Metrics (Manual Review)
- **Correctness**: Are conversions/calculations correct? (Pass/Fail)
- **Completeness**: All required fields present? (Pass/Fail)
- **Consistency**: Follows format guidelines? (Pass/Fail)
- **Profile adherence**: Respects user preferences? (Pass/Fail)
- **Overall quality**: 1-5 scale relative to baseline

### Quality Thresholds
- **Mechanical tasks** (import, card, shopping): ≥90% quality
- **Smart tasks** (suggest, research quick): ≥95% quality
- **Premium tasks** (research deep): 100% quality

## Success Criteria

A model is approved for a skill if:
1. Quality score ≥ threshold
2. No critical failures (wrong conversions, missing restrictions)
3. Cost savings ≥ target (50% for Haiku, 20% for Sonnet 3.5)

## Test Case Format

```json
{
  "skill": "import-recipe",
  "test_id": "import-recipe-01",
  "description": "Italian Osso Buco with unit conversions",
  "inputs": {
    "url": "https://example.com/osso-buco",
    "profile_path": "/Users/cmlee/meals/PROFILE.md"
  },
  "validation_checks": {
    "unit_conversion": {
      "400F": "200C",
      "2 cups": "480ml",
      "1 lb": "454g"
    },
    "title_format": "Osso Buco, Italian",
    "required_tags": ["italian", "beef", "braised", "featured-dish"],
    "must_exclude": ["allergy ingredients from profile"]
  },
  "quality_threshold": 0.90
}
```

## Next Steps

1. ✅ Create test harness structure
2. Write test case JSON files for Phase 1 skills
3. Create baseline execution script
4. Generate Sonnet 4.5 baselines
5. Run Haiku tests
6. Compare and report
7. Iterate on skill optimizations based on results

## Notes

- Test cases use real user data from `/Users/cmlee/meals/`
- Profile context always included for profile-aware skills
- Web URLs may need mocking for reproducible tests
- Manual quality review required for subjective assessments (creativity, cultural sensitivity)
