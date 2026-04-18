---
name: r-reduced-form
description: R econometrics — DiD, event study, IV, FE, RDD. fixest/did/rdrobust/modelsummary.
user_invocable: true
args: "[file.R] [task description]"
last_updated: 2026-03-30
---

# /r-reduced-form — R Reduced-Form Econometrics

**This is the default skill for econometric analysis.** Use R unless the user explicitly requests Stata.

## Core Workflow

1. Read the entire R script (or create new) to identify:
   - Estimation blocks (`feols`, `feglm`, `ivreg2`, `rdrobust`)
   - Fixed effects structure (`| fe1 + fe2` syntax in fixest)
   - Clustering level(s) (`cluster = ~id` or `vcov = ~id`)
   - Sample restrictions (`filter()`, `subset()`)

2. State clearly before editing:
   - Target estimand
   - Source of identifying variation
   - Expected sign and magnitude

3. Implement with these conventions:
   - Use `fixest` for all fixed-effects regressions (`feols`, `feglm`)
   - Use `did` package for Callaway & Sant'Anna staggered DiD
   - Use `rdrobust` for RDD
   - Use `modelsummary` or `etable()` for regression tables
   - Use `data.table` or `dplyr` for data manipulation
   - Use `ggplot2` for figures

## Preferred Package Map

| Task | Package | Function |
|------|---------|----------|
| OLS + FE | `fixest` | `feols(y ~ x | fe1 + fe2, cluster = ~id, data = df)` |
| IV/2SLS | `fixest` | `feols(y ~ 1 | fe \| x ~ z, data = df)` |
| Poisson FE | `fixest` | `feglm(y ~ x | fe, family = "poisson", data = df)` |
| Event study | `fixest` | `feols(y ~ i(time_to_treat, ref = -1) | id + time, data = df)` |
| Staggered DiD | `did` | `att_gt(yname, tname, idname, gname, data = df)` |
| Sun & Abraham | `fixest` | `feols(y ~ sunab(cohort, period) | id + time, data = df)` |
| RDD | `rdrobust` | `rdrobust(Y, X, c = 0)` |
| Regression table | `modelsummary` | `modelsummary(list(m1, m2, m3), output = "latex")` |
| fixest tables | `fixest` | `etable(m1, m2, m3, tex = TRUE, file = "results/table.tex")` |
| Coefficient plot | `fixest` | `coefplot(model)` or `iplot(model)` |
| Balance table | `modelsummary` | `datasummary_balance(~treatment, data = df)` |

## Checklist Before Writing Code

- [ ] Random seed: `set.seed(12345)` at script top
- [ ] Relative paths only — use `here::here()` or project-relative paths
- [ ] Clustering level matches unit of treatment assignment
- [ ] Fixed effects match specification in research plan
- [ ] Correct comparison group for DiD (never-treated vs. not-yet-treated)
- [ ] Pre-trends tested (event study coefficients or F-test)
- [ ] Output saved to `results/` (tables as `.tex`, figures as `.pdf`)
- [ ] Script numbered in pipeline order (`01_`, `02_`, etc.)

## Script Template

```r
# 01_main_estimation.R — [Description]
# Project: [Name]
# Date: YYYY-MM-DD

library(fixest)
library(data.table)
library(modelsummary)

set.seed(12345)

# --- Load data ---
df <- fread(here::here("data/processed/analysis_sample.csv"))

# --- Main specification ---
m1 <- feols(y ~ treat | id + time, cluster = ~id, data = df)

# --- Event study ---
m_es <- feols(y ~ i(time_to_treat, ref = -1) | id + time,
              cluster = ~id, data = df)

# --- Save results ---
etable(m1, tex = TRUE, file = here::here("results/tables/main_results.tex"))
iplot(m_es)
ggsave(here::here("results/figures/event_study.pdf"), width = 8, height = 5)
```

## Common Pitfalls

- `fixest` clusters with `cluster = ~var`, not `vcov = "cluster"` (the latter is the type, not the variable)
- `i()` in fixest requires factor or integer — check class before estimating
- `did::att_gt` requires panel data sorted by id and time
- `rdrobust` default bandwidth is MSE-optimal — report it, don't override without justification
- `modelsummary` needs explicit `stars` argument for significance markers
- Always check `fixef()` output to verify FE absorption worked correctly
