---
paths:
  - "**/*.py"
  - "**/*.do"
  - "**/*.m"
  - "**/*.tex"
  - "**/*.qmd"
  - "slides/**"
---

# Quality Gates & Scoring

## Thresholds

| Score | Gate | Action |
|-------|------|--------|
| 95+   | Excellence | Aspirational |
| 90+   | PR-ready | `gh pr create` |
| 80+   | Commit-ready | `git commit` |
| <80   | Blocked | Fix blocking issues first |

## Paper Format Gate (*.tex papers — runs before content scoring)

Format gate failures are **blocking** — no content score is computed if format gate fails.

| Check | Pass | Fail |
|-------|------|------|
| Citation count ≥ 10 | Citations found | Fewer than 10 → **BLOCKED** |
| No placeholder text | None found | Any TBD/TODO/XXX → **BLOCKED** |
| All figures exist | All files found | Any missing → **BLOCKED** |
| No unresolved references | No `???` found | Any `???` → **BLOCKED** |

If any check fails: score = 0 (blocked). Fix and re-run format gate before proceeding.

## Python Scripts (*.py)

| Severity | Issue | Deduction |
|----------|-------|-----------|
| Critical | Script errors on run | −100 |
| Critical | NaN/Inf in numerical outputs | −30 |
| Critical | Hardcoded absolute paths | −20 |
| Critical | Wrong moment conditions (domain) | −30 |
| High | Missing random seed | −10 |
| High | Non-reproducible (different runs differ) | −20 |
| High | Tests failing | −15 per failure |
| Medium | Missing docstrings on public functions | −3 |
| Medium | Lines > 120 chars | −1 per occurrence |

## Julia Scripts (*.jl)

| Severity | Issue | Deduction |
|----------|-------|-----------|
| Critical | Script errors on run | −100 |
| Critical | NaN/Inf in numerical outputs | −30 |
| Critical | Hardcoded absolute paths | −20 |
| High | Missing `Random.seed!` for stochastic code | −10 |
| High | No `Project.toml` (environment undeclared) | −10 |
| Medium | Non-reproducible across runs | −15 |

## Stata Do-Files (*.do)

| Severity | Issue | Deduction |
|----------|-------|-----------|
| Critical | Script errors on run | −100 |
| Critical | Wrong clustering level | −25 |
| Critical | Absolute paths | −20 |
| High | Missing `set seed` for bootstrap | −10 |
| High | Missing `version` declaration | −5 |
| High | Sample doesn't match paper description | −20 |
| Medium | No log file | −5 |

## MATLAB Scripts (*.m)

| Severity | Issue | Deduction |
|----------|-------|-----------|
| Critical | Script errors on run | −100 |
| Critical | NaN/Inf in results | −30 |
| High | Missing `rng(seed)` for stochastic code | −10 |
| High | VF not converged (check tol/iter) | −20 |
| Medium | Absolute paths | −15 |

## LaTeX Paper (*.tex)

| Severity | Issue | Deduction |
|----------|-------|-----------|
| Critical | Compilation failure | −100 |
| Critical | Undefined citations (???) | −15 each |
| High | Overfull \hbox > 10pt | −5 each |
| High | Broken \ref or \autoref | −10 |
| Medium | Bullet lists in results section | −3 |
| Minor | Em dashes in formal text | −1 each |

## Beamer Slides (*.tex in slides/)

| Severity | Issue | Deduction |
|----------|-------|-----------|
| Critical | Compilation failure | −100 |
| Critical | Equation overflow | −20 |
| Critical | Undefined citation | −15 |
| Major | Text overflow (overfull box > 5pt) | −5 each |
| Major | Label overlap in TikZ | −10 |
| Major | `\pause` used | −5 each |
| Minor | Font reduction blanket | −3 |

## Enforcement

- **Score < 80**: List blocking issues. Do NOT commit.
- **Score 80-89**: Commit allowed, warn about issues.
- **Score 90+**: PR ready.
- User can override with documented justification.

## Research Exploration (explorations/)

Threshold reduced to **60/100**. Focus on correctness, not polish.

## Tolerance Thresholds (Customize per project)

| Quantity | Tolerance | Note |
|----------|-----------|------|
| Point estimates | [e.g., 1e-6] | [Numerical precision] |
| Standard errors | [e.g., 1e-4] | [MC variability] |
| Acceptance rate (MCMC) | [0.2 - 0.5] | |
| Moment distance | [project-specific] | |
