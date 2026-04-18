---
paths:
  - "**/*.py"
  - "**/*.do"
  - "**/*.m"
  - "**/*.tex"
  - "scripts/**"
  - "stata/**"
---

# Verification Protocol

**Never report a task as "done" without actually verifying the output.**

## Mandatory Verification by File Type

### Python Scripts
```bash
python script.py 2>&1 | tail -20
python -m pytest tests/ -v --tb=short 2>&1 | tail -20
```
- Script runs without errors
- Expected output files exist and are non-empty
- No NaN/Inf: `python -c "import numpy as np; a=np.load('results/x.npy'); print(np.any(np.isnan(a)))"`

### Stata Do-Files
- Check log for `r(1)` errors or missing output files
- Verify output files at expected paths: `ls output/tables/ output/figures/`
- Sample size sanity check: does `obs` match expected?

### MATLAB Scripts
- Run and check for errors in console output
- Verify `.mat` output saved: `ls results/*.mat`
- Check for NaN/Inf in key outputs

### LaTeX / Beamer
```bash
# Full build sequence to resolve all references
pdflatex paper.tex && bibtex paper && pdflatex paper.tex && pdflatex paper.tex
# or
latexmk -pdf paper.tex
```
- PDF opens and is non-empty
- No `???` in output (unresolved references)
- No `Undefined control sequence` errors
- Check for `Overfull \hbox` warnings (> 5pt is a problem)

### Tests
```bash
python -m pytest tests/ -v 2>&1
```
- All tests pass (0 failures, 0 errors)

## Common Pitfalls

1. **LaTeX**: Single `pdflatex` run leaves `???` — always run full 3-pass sequence
2. **Python**: Script "runs" but output file is empty (check file size)
3. **Stata**: `quietly` block masks errors — check log file not just console
4. **MATLAB**: Non-convergence returns NaN silently — check values after run

## After Verification

Report: ✓ Verified OR ✗ Failed with exact error message and line number.
