# Test Harness Summary

## What We've Built

A comprehensive test framework to validate the cost optimization strategy for Braizent meal planner skills.

### Test Cases Created

1. **import-recipe** - 3 test cases
   - Italian Osso Buco (complex conversions)
   - Simple roasted chicken
   - Bread recipe (fractions, baking)
   - Target: Haiku with 70-75% cost savings

2. **add-to-shopping-list** - 3 test cases
   - Chicken and dumplings (Knuspr specific)
   - Multi-meal smart allocation
   - Vietnamese dish (store preferences)
   - Target: Haiku with 70-80% cost savings

3. **suggest-meal** - 4 test cases
   - Tuesday weeknight (quick vs. smart modes)
   - Saturday featured dish (web fallback)
   - Wednesday board gaming (scaling)
   - Target: Quick (Haiku) 90% savings, Smart (Sonnet 3.5) 40-50% savings

4. **research-recipe** - 3 test cases
   - Vietnamese Pho (quick vs. deep)
   - Italian Carbonara (quick)
   - Target: Quick (Sonnet 3.5) 75-80% savings, Deep (unchanged)

5. **quick-staple** - 2 test cases
   - Pork chops (conversational vs. batched)
   - Roasted chicken (profile context)
   - Target: Haiku with 70-75% cost savings

## Testing Approach

### Phase 1: Baseline Generation (Sonnet 4.5)
Run all test cases with current Sonnet 4.5 implementation to establish:
- Quality baseline (what "100%" looks like)
- Cost baseline
- Token usage baseline
- Execution time baseline

### Phase 2: Optimization Implementation
Add the optimization modifications to skills:
- **A1-A3**: import-recipe (tables, algorithms)
- **A4-A5**: add-to-shopping-list (lookup tables)
- **C2**: suggest-meal (side dish templates)
- **D1**: quick-staple (batched questions)
- **F1-F2**: Multi-tier modes for research-recipe and suggest-meal

### Phase 3: Comparison Testing
Run optimized versions through all test cases:
- Haiku tests (for mechanical skills)
- Sonnet 3.5 tests (for smart modes)
- Compare outputs vs. baseline
- Measure cost savings
- Assess quality degradation

### Phase 4: Analysis & Iteration
Review results:
- Are quality thresholds met? (≥90% mechanical, ≥95% smart)
- Are cost targets achieved? (45-60% overall savings)
- Where does quality degrade?
- What needs refinement?

## Expected Outcomes

### Phase 1 Skills (Mechanical → Haiku)
| Skill | Baseline Cost | Target Cost | Savings | Quality |
|-------|---------------|-------------|---------|---------|
| import-recipe | $0.40-0.60 | $0.10-0.15 | 70-75% | ≥90% |
| add-to-shopping-list | $0.75-1.00 | $0.15-0.25 | 70-80% | ≥90% |
| recipe-card | $0.20-0.30 | $0.05 | 75-80% | ≥90% |
| quick-staple (opt) | $0.40-0.60 | $0.10-0.15 | 70-75% | ≥90% |

**Phase 1 Total**: 25-35% overall cost reduction

### Phase 2 Skills (Multi-Tier)
| Skill | Mode | Model | Cost | Savings | Quality |
|-------|------|-------|------|---------|---------|
| suggest-meal | Quick | Haiku | $0.10-0.15 | 90% | ≥90% |
| suggest-meal | Smart | Sonnet 3.5 | $0.80-1.00 | 40-50% | ≥95% |
| research-recipe | Quick | Sonnet 3.5 | $0.60-0.80 | 75-80% | ≥95% |
| research-recipe | Deep | Sonnet 4.5/Opus | $3-5 | 0% | 100% |

**Phase 1 + 2 Total**: 45-60% overall cost reduction

## Key Success Metrics

### Must Achieve
- ✅ Overall cost reduction: 45-60%
- ✅ No critical failures (wrong conversions, missed restrictions)
- ✅ Quality thresholds met for each skill type

### Nice to Have
- Faster execution time with cheaper models
- Improved consistency (explicit rules)
- User satisfaction maintained or improved

## What Makes This Work

### 1. Explicit Instructions
Moving from "convert units" to "use this exact table" makes execution mechanical.

### 2. Profile Context
Including full PROFILE.md makes cheaper models profile-aware.

### 3. Smart Trade-offs
- Keep expensive intelligence where it matters (cultural sensitivity, quantity allocation)
- Use cheap models for mechanical tasks (conversions, tags, templates)
- Let users choose cost/quality trade-off (quick vs. deep modes)

### 4. Real Data Testing
Using actual user data (/Users/cmlee/meals/) ensures tests reflect real usage:
- 62 existing recipes
- Real profile (2 adults, Wednesday guests, Knuspr/Rewe shopping)
- Edge cases from actual meal planning (Sunday closed stores, Pollofino, etc.)

## Next Steps

1. ✅ **Test cases created** - comprehensive coverage
2. **Implement optimizations** - add tables/templates to skills
3. **Run baseline tests** - establish Sonnet 4.5 quality/cost
4. **Run optimized tests** - test Haiku/Sonnet 3.5 versions
5. **Compare & analyze** - validate savings and quality
6. **Iterate** - refine based on results
7. **Deploy** - roll out optimized skills

## Files Created

```
test-harness/
├── README.md                          # Test harness documentation
├── SUMMARY.md                         # This file
├── test-cases/
│   ├── import-recipe.json            # 3 test cases
│   ├── add-to-shopping-list.json     # 3 test cases
│   ├── suggest-meal.json             # 4 test cases
│   ├── research-recipe.json          # 3 test cases
│   └── quick-staple.json             # 2 test cases
└── [TODO: execution scripts, results directories]
```

## Critical Features to Preserve

Even with aggressive optimization, these MUST work correctly:

### Safety-Critical
- ✅ Dietary restriction checking (add-to-shopping-list, all meal skills)
- ✅ Unit conversion accuracy (import-recipe)
- ✅ Store/day availability (add-to-shopping-list: Sunday closed)

### High-Value Features
- ✅ Smart quantity allocation (add-to-shopping-list)
- ✅ Cultural sensitivity (research-recipe deep mode)
- ✅ Profile-aware suggestions (all skills)
- ✅ Web fallback (suggest-meal smart mode)

### User Experience
- ✅ Consistency (tags, formats, structure)
- ✅ User choice (quick vs. smart/deep modes)
- ✅ Speed acceptable for use case (quick-staple should be quick)

## Cost Breakdown (Projected)

### Current State
- **Average execution**: $1.50
- **Monthly usage** (estimated 50 executions): $75
- **Heavy users**: Could be $100-200/month

### After Phase 1
- **Average execution**: $1.00-1.20
- **Monthly usage**: $50-60
- **Savings**: ~$20-25/month (20-30%)

### After Phase 2
- **Average execution**: $0.70-0.90
- **Monthly usage**: $35-45
- **Savings**: ~$30-40/month (40-50%)
- **Heavy users**: $50-90/month (vs. $100-200)

### ROI
- **Implementation cost**: 4-6 weeks development
- **Ongoing savings**: $30-40/month average user
- **Payback**: Immediate for heavy users, 3-6 months for average users
- **Benefit**: Price becomes sustainable for regular use

## Conclusion

This test harness provides:
1. **Confidence** - validate optimizations work before deploying
2. **Measurability** - quantify cost savings and quality impact
3. **Iterability** - identify what works and what needs refinement
4. **Documentation** - clear record of decisions and trade-offs

The goal is **45-60% cost reduction with minimal UX degradation**, achieved through:
- Template hardening (explicit instructions)
- Multi-tier approach (user choice)
- Profile context (smart defaults)
- Preserving high-value intelligence

Next: Implement Phase 1 optimizations and run first test suite.
