# Pre-Analysis Plan: [Short Title]
**Date locked:** YYYY-MM-DD HH:MM
**Checksum:** [run: sha256sum quality_reports/paps/YYYY-MM-DD_topic.md]
**Status:** LOCKED / DRAFT

> ⚠️ Finalize and checksum BEFORE any data is accessed or code is run. Once locked, do not edit; create a new version (v2) if the design changes.

---

## 1. Research Question
**Primary question:** [One sentence: "What is the effect of X on Y?"]
**Policy context:** [Policy/intervention, jurisdiction, time period]
**Gap in literature:** [Why unanswered? Contribution]

---

## 2. Theoretical Framework
**Primary mechanism:** [Expected channel; sign and magnitude]
**Alternative mechanisms:** [2–3 competing explanations; how they differ]
**Null hypothesis:** [Meaning of zero effect]

---

## 3. Data Specification
**Dataset:** [Name, version, source URL or file path]
**API endpoint (if applicable):** [Exact URL template, e.g., https://api.census.gov/data/{YEAR}/acs/acs1/pums]
**Time period:** [Start year – End year]
**Unit of observation:** [Individual / firm / county / state-year / etc.]
**Sample restrictions:**
- Age: [e.g., 18–64]
- Industry/occupation: [e.g., NAICS 72, Census occ codes 4500–4540]
- Other: [employed full-time, non-military, etc.]

**Key variable names (exact column names):**

| Variable | Column name | Description |
|----------|-------------|-------------|
| Primary outcome | [e.g., WKHP] | Hours worked per week |
| Secondary outcome | [e.g., ESR] | Employment status recode |
| Treatment indicator | [e.g., treated_state] | 1 if state passed policy by year t |
| Key control | [e.g., AGEP] | Age |
| [add rows] | | |

**Survey weights:** [PWGTP / PERWT / none; justify]

---

## 4. Empirical Strategy
**Estimator:** [DiD / staggered DiD / IV / RDD / Diff-in-RD / structural SMM]

**Regression equation (LaTeX):**

Y_{ist} = \alpha + \beta \cdot Treated_{st} + X_{ist}'\gamma + \delta_s + \lambda_t + \varepsilon_{ist}

where:
- Y_{ist} = [outcome for individual i in state s at time t]
- Treated_{st} = [treatment indicator]
- X_{ist} = [control vector]
- \delta_s = state fixed effects
- \lambda_t = year fixed effects

**Standard errors:** Clustered at [state / county / firm]; justify.
**Fixed effects:** [State FE, year FE; absorbed via reghdfe / feols / csdid]

*For staggered DiD (if applicable):*
- Estimator: [Callaway-Sant'Anna / Sun-Abraham / Borusyak et al.]
- Package: [csdid (Stata) / did (R) / staggered (R)]
- Never-treated group: [defined? comparison group?]

---

## 5. Outcome Variables
**Primary outcome:** [Variable, unit, expected sign, expected magnitude]
**Secondary outcomes (pre-specified):**
1. [Variable 2]
2. [Variable 3]

**Null if no effect:** [Expected value under H0]

---

## 6. Heterogeneity Analysis (pre-specified)
Run separately for each subgroup:

| Subgroup | Variable | Split | Hypothesis |
|----------|----------|-------|-----------|
| [e.g., Parental status] | [e.g., PAOC > 0] | Binary | [Larger effect for parents] |
| [e.g., Low education] | [e.g., SCHL < 16] | Binary | [Binding for less-educated] |

---

## 7. Robustness Checks (pre-specified)
- [ ] Event study: plot coefficients for t-k to t+k; check pre-trends
- [ ] Placebo: apply treatment to [unaffected group / pre-period]; expect null
- [ ] Alternative clustering: cluster at [county/industry]; compare SEs
- [ ] Alternative sample: [restrict/expand sample]
- [ ] Alternative estimator: [compare primary to alternative DiD estimator]

---

## 8. Technical Specification (for analysis code generation)
**Language:** [R / Python / Stata / MATLAB]
**Key packages:**
- Data fetching: [httr, requests, censusapi]
- Estimation: [csdid, fixest, reghdfe, ivreghdfe]
- Tables: [modelsummary, estout, outreg2, stargazer]
- Figures: [ggplot2, matplotlib, pgfplots]

**Script execution order:**
1. `[fetch_data.py / 01_clean.do]` — download and clean data
2. `[analyze_main.py / 02_analysis.do]` — run primary regressions
3. `[create_figures.py / 03_figures.do]` — generate figures

**Expected outputs:**
| Output file | Script that generates it | Contents |
|-------------|--------------------------|----------|
| results/table1_main.tex | analyze_main.py | Main DiD estimates |
| results/fig_event_study.pdf | create_figures.py | Event study plot |
| [add rows] | | |

**Data caching:** [Yes — cache raw API response to data/raw/census_cache.json to avoid re-downloading]

---

## 9. Identification Assumptions
**Required for causal interpretation:**
1. [Parallel trends]
2. [No anticipation]
3. [SUTVA / no spillovers]

**How each is tested:**
1. [Pre-trends in event study; placebo on pre-period]
2. [Exclude 1–2 years before policy adoption]
3. [Exclude bordering states / test for spatial spillovers]

---

## Checksum Instructions
After finalizing (before any data access):
```bash
sha256sum quality_reports/paps/YYYY-MM-DD_topic.md
# Copy the hash into the Checksum field
# Then commit: git add quality_reports/paps/ && git commit -m "Lock PAP: [topic]"
```
A committed, checksummed PAP is the only pre-registration artifact used in this project.
