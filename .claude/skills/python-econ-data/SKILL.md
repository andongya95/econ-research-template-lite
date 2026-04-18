---
name: python-econ-data
description: Python data cleaning, panel construction, and export for regression or estimation.
last_updated: 2026-04-13
---

## Skill Usage Guidelines

**Documentation Policy:**
- Do NOT create new standalone markdown documentation files (summaries, status reports, etc.) without explicit user request
- Update existing project files or session logs instead
- Consolidate updates into existing documentation structure

**Version Tracking:**
- The `last_updated` field in the frontmatter above shows when this skill was last modified
- When making ANY changes to this skill file, update the `last_updated` field to the current date (YYYY-MM-DD format)
- Use command-line tools to verify the current date if needed

## Core workflow

1. Identify:
   - Unit of observation
   - Merge keys
   - Time index
   - Panel structure

2. Propose transformation plan before editing.

3. Implement with explicit validation checks.

## Data integrity rules

- Assert key uniqueness before and after merges
- Log row counts at each step
- Track missingness explicitly
- Avoid silent type coercion

## Outputs

- Regression-ready datasets
- Structural-ready inputs (states, choices, shocks)
- Deterministic exports for Stata/MATLAB

### Merge Audit Artifact

For any panel build involving ≥2 source merges, produce a merge audit CSV alongside
the panel output. One row per source file merged. Required columns:

| Column | Content |
|---|---|
| `source_file` | filename of the merged source |
| `rows_in` | row count of source before any filter |
| `rows_after_filter` | row count after sample restriction (if any) |
| `merge_type` | `1:1`, `m:1`, or `1:m` |
| `matched` | rows successfully matched to master |
| `unmatched` | rows not matched (flag if unexpectedly high) |
| `note` | any coverage gap or expected sparsity explanation |

Final row: summary of the merged panel (total rows, total columns, key coverage,
duplicate key count — must be 0).

Save to: `results/[task]/[name]_audit.csv`

### Hold-Out Documentation

For any panel build, explicitly list source files or variable groups intentionally
excluded from the current pass, with reasons. Add as a named section in the task
note or script header:

```
## Hold-Outs (not merged in this pass)
- [filename] — reason: monthly granularity, held for robustness
- [filename] — reason: not in core variable set for first pass
- [variable group] — reason: reserved for second-pass heterogeneity analysis
```

This makes the data scope boundary explicit and prevents silent omission.

## Related skills

- **econ-orchestrator**: Multi-stage workflows; coordinate with Stata/MATLAB/TeX
- **stata-reduced-form**, **structural-estimation**: Downstream consumers of regression-ready data
