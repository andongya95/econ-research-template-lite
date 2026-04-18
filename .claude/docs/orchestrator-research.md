---
paths:
  - "scripts/**"
  - "stata/**"
  - "explorations/**"
  - "src/**"
---

# Research Orchestrator (Simplified)

For scripts, simulations, data analysis, and exploration — use this simplified loop instead of the full multi-agent orchestrator.

## The Simple Loop

```
Plan approved → orchestrator activates
  │
  Step 1: IMPLEMENT — Execute plan steps
  │
  Step 2: VERIFY — Run code, check outputs
  │         Python: script runs + no NaN/Inf + tests pass
  │         Stata: script runs + output files created + sample checks
  │         MATLAB: script runs + no NaN/Inf + results saved
  │         If fails → fix → re-verify (max 2 retries)
  │
  Step 3: SCORE — Apply quality-gates rubric
  │
  └── Score >= 80?
        YES → Done (commit when user signals)
        NO  → Fix blocking issues, re-verify, re-score
```

**No multi-round agent reviews. No parallel spawning. Just: write, test, done.**

## Verification Checklist

- [ ] Script runs without errors
- [ ] All imports/packages resolve
- [ ] No hardcoded absolute paths
- [ ] Seed set for stochastic code
- [ ] Output files at expected paths and non-empty
- [ ] No NaN/Inf in numerical results
- [ ] Quality score >= 80

## Parallel Agents for Research (when useful)

For independent subtasks (reading 3 papers, running 3 simulations), spawn agents in parallel via Task tool. Max 3 parallel agents. Don't parallelize if task B depends on task A's output.

## Explorations

Use 60/100 threshold. Skip formal planning — just a 2-minute research value check: "Does this improve the project?" If yes: proceed. If maybe: explore. If no: skip.
