---
name: analysis-spec
description: Scaffold a regression spec-design note before coding — spec ladder, variable curation, and results log.
user_invocable: true
args: "[variable_inventory_path] [task description]"
last_updated: 2026-04-13
allowed-tools: Read, Write, Glob, Grep
---

# /analysis-spec — Regression Spec-Design Note

Produces a structured spec-design task note (`task_notes/NN_analysis.md`) **before any
code is written**. Mirrors the discipline in `selection_workflow_template/task_notes/02_analysis.md`.

---

## When to Use

- Starting a new regression or panel analysis
- Before writing any estimation code
- After `/research-plan` and `/resolve-conditions`, before `/r-reduced-form`

---

## Inputs Required

Elicit all six before drafting the note:

1. **Dependent variable** — name and panel column
2. **Estimation year / cross-section** — the year or period used for cross-section collapse
3. **Time-varying control window** — e.g. "1995–1999 means"
4. **Variable inventory source** — file path OR inline list of candidate variables by concept group
5. **Clustering level** — unit at which standard errors are clustered
6. **Sample scheme(s)** — comparisons to make (e.g. keep vs. drop a subgroup)

---

## Skill Workflow

```
1. Read CLAUDE.md and any existing research plan in quality_reports/plans/
2. Read variable inventory file if provided; else ask user to supply concept groups
3. Elicit all 6 required inputs above
4. Draft the task note with all 10 sections (see Output Structure below)
5. Auto-number NN from existing files in task_notes/ (01, 02, 03, ...)
6. Save to task_notes/NN_analysis.md
7. Display to user and request approval before any code is written
```

**Do not write any estimation code until the user approves the spec note.**

---

## Output Document Structure

The produced task note contains these 10 sections in order:

### 1. Goal
One sentence stating the estimand and the sample.

### 2. Active Inputs and Code
- Panel path
- Variable inventory path
- Active code path
- Output folder

### 3. Outcome and Sample
- Dependent variable and column name
- Intensity follow-up variable (if any)
- Estimation year / cross-section definition
- Time-varying control window (years)
- Sample discipline rule (who is included/excluded and why)
- Blank placeholders: `N = ___` (fill after first run)

### 4. Variable Curation
Subsections by concept group (e.g., Administrative/Topography, Hydrologic Exposure,
Socioeconomic/Land Use). Within each group:
- One representative variable selected per concept — state selection rationale briefly
- **Reserved for Robustness** block: list close substitutes deferred, with stated reasons

### 5. Spec Ladder
Nested A → B → C → D table. Each column defined by concept block added, not by individual
variable list. Implementation rules attached inline:
- Transform convention (asinh for skewed counts, log for rates/prices)
- Clustering level and justification
- Cross-section construction rule
- Exception handling (e.g., how to handle zeros before asinh)

### 6. Implementation Notes
- Transform convention with rationale
- Standard error clustering justification
- Cross-section construction rule (e.g., collapse to means over window)

### 7. Preliminary Read *(fill after first run)*
Blank section with sub-headers:
- Coefficient stability across specs
- R² gain per block added
- Narrative interpretation
- Sample-design conclusion

### 8. Search Results *(optional)*
Blank section for protected-sample or full-factorial variable search. Include ranking
criteria when used: sign constraints → weak significance → R².

### 9. Nested Column Follow-Up *(optional)*
Column structure by concept block, variable mapping per column, approved command,
output paths.

### 10. Current Status
Execution log — one row per run attempt:
- Command run
- Output paths produced
- Run status (SUCCESS / FAILED + error summary)

---

## Task Note Template

```markdown
# Analysis Spec: [Task Description]
**Date:** YYYY-MM-DD
**Research plan:** quality_reports/plans/YYYY-MM-DD_[paper]-research-plan.md

---

## 1. Goal
[One sentence: estimand + sample]

---

## 2. Active Inputs and Code
- Panel: `data/processed/[panel].csv`
- Variable inventory: `[path or "inline — see Section 4"]`
- Code: `R/[NN]_analysis.R` *(to be created)*
- Output: `results/[task]/`

---

## 3. Outcome and Sample
- **Dependent variable:** [name] (`[column]`)
- **Estimation year:** [YYYY]
- **Control window:** [YYYY–YYYY] means
- **Sample rule:** [who is included; exclusion criteria]
- **N (cross-section):** ___ *(fill after first run)*
- **N (estimation sample):** ___ *(fill after first run)*

---

## 4. Variable Curation

### [Concept Group 1]
- **Selected:** `[var]` — [brief rationale]
- *Reserved for robustness:* `[alt_var]` — [reason deferred]

### [Concept Group 2]
- **Selected:** `[var]` — [brief rationale]
- *Reserved for robustness:* `[alt_var]` — [reason deferred]

### Reserved for Robustness (cross-cutting)
| Variable | Reason Deferred |
|----------|----------------|
| `[var]` | [reason] |

---

## 5. Spec Ladder

| Spec | Columns Added | Block Label |
|------|---------------|-------------|
| A | (none — outcome + treatment only) | Baseline |
| B | + [Concept Group 1 var] | [Label] |
| C | + [Concept Group 2 var] | [Label] |
| D | + [Concept Group 3 var] | [Label] |

**Implementation rules:**
- Transform: asinh() for skewed counts; log() for rates/prices
- Clustering: [level] — [justification]
- Cross-section: collapse [window] means per [unit]
- Exceptions: [e.g., zeros → add 1 before log; or use asinh directly]

---

## 6. Implementation Notes
- **Transform:** [convention + rationale]
- **SE clustering:** [level] — [why appropriate]
- **Cross-section construction:** [rule for collapsing panel to estimation sample]

---

## 7. Preliminary Read *(fill after first run)*

### Coefficient stability
[fill]

### R² gains per block
| Block added | ΔR² |
|-------------|-----|
| B | |
| C | |
| D | |

### Narrative interpretation
[fill]

### Sample-design conclusion
[fill]

---

## 8. Search Results *(optional — fill if conducting variable search)*

Ranking criteria: sign constraint satisfied → p < 0.10 → R² gain

| Rank | Variable | Sign OK? | p-value | ΔR² |
|------|----------|----------|---------|-----|
| | | | | |

---

## 9. Nested Column Follow-Up *(optional)*

| Column | Block | Variables | Command | Output |
|--------|-------|-----------|---------|--------|
| | | | | |

---

## 10. Current Status

| Step | Command | Output Path | Status |
|------|---------|-------------|--------|
| | | | |
```

---

## Approval Gate

After drafting, present the note and explicitly ask:

> "Does this spec note look correct? Approve to proceed to code, or request changes."

Do not write any R/Python/Stata code until the user approves the spec note.

---

## Notes

- Output location: `task_notes/` in the project root (created on demand)
- Auto-number: scan `task_notes/` for existing files; use the next available `NN`
- No hardcoded project paths — all paths use `here::here()` or relative notation
- Sections 8 and 9 are optional — include only if the task involves variable search or nested column follow-up
