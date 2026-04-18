---
scope: global
---

# R as Default Econometric Language

When generating econometric analysis code, **always use R** unless the user explicitly requests another language.

## Applies to

DiD, event studies, IV/2SLS, fixed effects, panel regressions, RDD, heterogeneity analysis, regression tables, pre-trend tests, and all reduced-form econometrics.

## Preferred R packages

| Task | Package |
|------|---------|
| Fixed effects / IV | `fixest` (`feols`, `feglm`) |
| Staggered DiD | `did` (Callaway & Sant'Anna), `did2s` |
| RDD | `rdrobust` |
| Regression tables | `modelsummary`, `etable` (fixest built-in) |
| Event studies | `fixest` with `i()` syntax |
| Data wrangling | `data.table` or `dplyr` |
| Figures | `ggplot2` |

## When NOT R

- User explicitly says "use Stata" or "write a .do file"
- Structural estimation → Python (JAX) or MATLAB per `/structural-estimation`
- Game theory derivation → SymPy (Python) per `/primenash-game-theory`
- Data cleaning from raw sources → Python if format requires it (JSON, API, web scraping)
