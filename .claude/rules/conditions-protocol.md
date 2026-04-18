---
paths: ["quality_reports/plans/**"]
---

# Pre-Execution Conditions Protocol

Before writing any analysis code, resolve all 5 conditions. Document resolutions in:
`quality_reports/plans/YYYY-MM-DD_[paper]-conditions.md`

**All 5 must be RESOLVED before coding begins.** A condition is RESOLVED when both an issue and a one-sentence resolution are written down. UNRESOLVED conditions block implementation.

---

## The 5 Conditions

### Condition 1 — Data Measurement
**Issue:** Is the outcome variable measured correctly?
- Confirm units (e.g., counts vs. rates vs. logs)
- Confirm timing (date of service vs. date of payment vs. date of record)
- Confirm definition (what exactly is being measured — confirm against codebook)

**Resolution:** "Outcome is measured as [X], sourced from [field/variable], using [service/payment/record] date."

### Condition 2 — Treatment Timing
**Issue:** When does treatment begin?
- Confirm first-complete-exposure period (monthly, quarterly, annual?)
- Handle boundary cases: what if a policy takes effect mid-period?
- Define how partial periods are coded

**Resolution:** "Treatment begins in [period]. Mid-period cases are coded as [treated in next full period / prorated / excluded]."

### Condition 3 — Causal Inference Approach
**Issue:** Is the estimator correctly specified for the design?
- Confirm estimator choice (TWFE, CS-DiD, 2SLS, rdrobust, etc.)
- Confirm comparison group (never-treated, waitlisted, clean controls)
- Confirm pre-trend testing plan (how many pre-periods? what test?)
- Note if staggered adoption requires heterogeneity-robust estimator

**Resolution:** "Estimator is [X]. Comparison group is [Y]. Pre-trends tested via [Z]."

### Condition 4 — Confounding Control
**Issue:** What are the top threats to identification?
- List up to 3 specific threats (not generic)
- Confirm how each is addressed (fixed effects, controls, robustness check, data limitation)

**Resolution:** "Top threats: (1) [threat] → addressed by [method]; (2) [threat] → addressed by [method]; (3) [threat] → acknowledged as limitation."

### Condition 5 — Comparability
**Issue:** Are treated and control units comparable?
- Check pre-treatment balance on key covariates
- Plan for imbalance (entropy balancing, reweighting, restricted sample)
- Confirm control group is not undergoing a contemporaneous shock

**Resolution:** "Control group is comparable on [key dimensions]. Balance check: [planned]. Imbalance addressed by [method / acknowledged as limitation]."

---

## Document Format

```markdown
# Pre-Execution Conditions: [Paper Name]
**Date:** YYYY-MM-DD
**Research plan:** quality_reports/plans/YYYY-MM-DD_[paper]-research-plan.md

| Condition | Status | Issue | Resolution |
|-----------|--------|-------|------------|
| 1. Data Measurement | RESOLVED | [issue] | [resolution] |
| 2. Treatment Timing | RESOLVED | [issue] | [resolution] |
| 3. Causal Inference Approach | RESOLVED | [issue] | [resolution] |
| 4. Confounding Control | RESOLVED | [issue] | [resolution] |
| 5. Comparability | RESOLVED | [issue] | [resolution] |

## Notes
[Any additional decisions made during conditions resolution]
```

Status options: **RESOLVED** | **UNRESOLVED** (blocks coding) | **N/A** (with justification)
