---
scope: global
---

# Session Logging

Three triggers. All logs: `quality_reports/sessions/YYYY-MM-DD_description.md`.

## Trigger 1: After Plan Approval

Create session log immediately with: Goal, Approach, Rationale (incl. rejected alternatives), Key context.
Do this BEFORE implementation — context is richest right after approval.

## Trigger 2: Incremental (most important)

Append 1-3 lines whenever a design decision is made, a problem is solved, the approach deviates, or the user corrects something.
**Do NOT batch.** Log immediately — context compression will erase unlogged decisions.

## Trigger 3: End of Session

Add: What was accomplished, open questions/blockers, quality scores, next steps.

## Log Format

```markdown
# Session Log: [short description]
**Date:** YYYY-MM-DD
**Goal:** [one sentence]

## Plan Summary
[2-3 sentences]

## Rationale
[Why this approach. Alternatives considered: ...]

## Progress Log
- [HH:MM] Decision: ...
- [HH:MM] Problem found: ... → Solution: ...

## End of Session
**Accomplished:** ...  **Open questions:** ...  **Next steps:** ...

## Judgment Divergence (append when PI overrides a reviewer)
- [agent] flagged X → PI dismissed (reason) → action taken
- [agent] missed Y → PI caught it → action taken
```

## Key Rules

- Git commits record **what**; session logs record **why**.
- Plans go in `quality_reports/plans/`; logs go in `quality_reports/sessions/`. The `plan-path-guard` hook enforces this.
- Human gates (QUESTION_SELECTED, FINAL_APPROVAL): log in both session log and `PIPELINE_STATE.md`. Never auto-generate gate entries.
