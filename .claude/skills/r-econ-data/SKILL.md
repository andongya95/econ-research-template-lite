---
name: r-econ-data
description: R data cleaning, panel construction, merges, reshaping. data.table/dplyr wrangling.
user_invocable: true
args: "[file.R] [task description]"
last_updated: 2026-04-13
---

# /r-econ-data — R Data Construction for Economics

## Core Workflow

1. Identify:
   - Unit of observation (individual, firm-year, county-month)
   - Merge keys (identifiers across datasets)
   - Time index (date, year-quarter, period)
   - Panel structure (balanced vs. unbalanced)

2. Propose transformation plan before editing.

3. Implement with explicit validation checks at each step.

## Preferred Packages

| Task | Package | Function |
|------|---------|----------|
| Fast I/O | `data.table` | `fread()`, `fwrite()` |
| Reshaping | `data.table` | `melt()`, `dcast()` |
| Merges | `data.table` | `merge(x, y, by = ..., all.x = TRUE)` |
| String cleaning | `stringr` | `str_trim()`, `str_to_lower()` |
| Date parsing | `lubridate` | `ymd()`, `mdy()`, `floor_date()` |
| Missing data | base R | `is.na()`, `complete.cases()` |
| Panel checks | `plm` | `is.pbalanced()`, `pdim()` |
| Summary stats | `modelsummary` | `datasummary()`, `datasummary_skim()` |
| Export to Stata | `haven` | `write_dta()` |
| Export to CSV | `data.table` | `fwrite()` |

## Validation Checklist

After every major operation, verify:

- [ ] Row count: `nrow(df)` matches expectation (document expected N)
- [ ] No unintended duplicates: `anyDuplicated(df, by = key_vars) == 0`
- [ ] Merge diagnostics: report matched/unmatched counts from each side
- [ ] Missing values: `colSums(is.na(df))` for key variables
- [ ] Variable types correct: `str(df)` or `sapply(df, class)`
- [ ] Panel balance: `plm::is.pbalanced(df, index = c("id", "time"))`
- [ ] Value ranges plausible: `summary(df[, .(var1, var2)])` for key variables

## Script Template

```r
# 01_clean_data.R — [Description]
# Project: [Name]
# Date: YYYY-MM-DD

library(data.table)
library(haven)

set.seed(12345)

# --- Load raw data ---
raw <- fread(here::here("data/raw/source_data.csv"))
cat("Raw rows:", nrow(raw), "\n")

# --- Clean ---
df <- copy(raw)
df[, id := as.character(id)]
df[, date := as.Date(date)]

# --- Validate ---
stopifnot(anyDuplicated(df, by = c("id", "date")) == 0)
cat("Clean rows:", nrow(df), "Unique IDs:", uniqueN(df$id), "\n")

# --- Export ---
fwrite(df, here::here("data/processed/analysis_sample.csv"))
write_dta(df, here::here("data/processed/analysis_sample.dta"))
cat("Done. Exported to data/processed/\n")
```

### Merge Audit Artifact

For any panel build with ≥2 source merges, write a merge audit CSV alongside the
panel. One row per source merged. Required columns: `source_file`, `rows_in`,
`rows_after_filter`, `merge_type`, `matched`, `unmatched`, `note`. Final row: panel
summary (total rows, columns, key coverage, duplicate key count = 0).

In R, collect audit rows into a `data.table` and export with `fwrite()`:

```r
audit <- rbindlist(merge_log)  # list of one-row data.tables per source
audit <- rbind(audit, panel_summary_row)
fwrite(audit, here::here("results/[task]/[name]_audit.csv"))
```

Save to: `results/[task]/[name]_audit.csv`

### Hold-Out Documentation

List any source files or variable groups intentionally excluded from the current
build pass. Record in the task note and as a comment block in the script:

```r
# HOLD-OUTS (not merged in this pass):
# - source_monthly.csv  : monthly granularity — held for robustness
# - source_alt.csv      : alternative measure — reserved for second pass
```

### Output Conventions

- **Iterative analysis passes:** save each pass to a numbered subfolder:
  `results/[task]/01_prelim/`, `02_robustness/`, `03_final/`
- **Final shareable outputs:** copy to `results/keyresults/` — this folder holds
  only publication-ready tables and figures, not working outputs

## Common Pitfalls

- `merge()` in data.table defaults to inner join — use `all.x = TRUE` for left join
- `fread()` auto-detects types — verify dates aren't read as strings
- Panel gaps: `CJ()` (cross-join) to create balanced panel skeleton before merging
- Character encoding: specify `encoding = "UTF-8"` in `fread()` for non-ASCII data
- Large files: `data.table` is 10-100x faster than `dplyr` for >1M rows — prefer it
