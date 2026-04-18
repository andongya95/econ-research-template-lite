---
paths: ["quality_reports/plans/**", "quality_reports/sessions/**"]
---

# Plan-First Workflow

For any task touching >2 files or >30 min work, plan before coding.

## Protocol

1. **Enter Plan Mode** — use `EnterPlanMode`
2. **Check MEMORY.md** — read `[LEARN]` entries relevant to this task
3. **Requirements spec** (vague tasks >1hr or >3 files): ask 3-5 clarifying questions, create `quality_reports/specs/YYYY-MM-DD_description.md` with MUST/SHOULD/MAY, get approval
4. **Draft the plan** — what changes, which files, in what order, with **success criteria per step**
5. **Save to disk** — `quality_reports/plans/YYYY-MM-DD_short-description.md`
6. **Present to user** — wait for approval
7. **Exit plan mode** — only after approval
8. **Save initial session log** — capture goal and context while fresh
9. **Implement via orchestrator** — see orchestrator-protocol.md

## Success Criteria (Sprint Contracts)

Each plan step must have testable acceptance criteria written **before** implementation:

```markdown
## Step N: [description]
Files: [list]
### Success Criteria
- [ ] [Specific, verifiable condition]
- [ ] [Output condition — format, values, file existence]
- [ ] [Runtime condition — performance, no errors]
```

Evaluators verify against these criteria, not just generic rubrics. The verifier agent checks each criterion explicitly and reports PASS/FAIL per item.

## Plans on Disk

Plans survive context compression — always save to `quality_reports/plans/`.
Format: Status (DRAFT/APPROVED/IN_PROGRESS/COMPLETED), approach, files to modify, success criteria, verification.

## After Compression

First action: read CLAUDE.md + most recent plan + `git log --oneline -5`.

## Never Ask the User to Restart

Do NOT tell the user to "start a fresh session", "continue in a new conversation", or "run this in the next session." Instead:

- **Large implementation:** Spawn Agent subagents to do the work — each gets fresh context
- **Research/exploration:** Spawn Explore agents
- **Context pressure:** Stop any polling loops, save state to plan file, then auto-compaction will reclaim space — read the plan back and continue
- **Overnight runs:** Write `quality_reports/handoff.json` and let `run-autonomous.sh` continue

The user should never need to manually restart a session to continue work.

## Routing Note Convention (multi-step tasks)

When a task has two or more child steps where step N depends on step N-1 output,
use a numbered task note hierarchy instead of a single plan file:

- `task_notes/00_overview.md` — routing note only: defines the split, names the
  child files, states the dependency chain. Does NOT log implementation detail.
- `task_notes/01_<step>.md`, `task_notes/02_<step>.md`, … — one child task file
  per step; each records its own goal, inputs, implementation notes, execution
  history, and review dispositions.

When to use:
- ≥2 child steps with data dependency between them (e.g. data build → analysis)
- Each child step is likely to span multiple sessions or runs

When NOT to use:
- Single-step tasks or parallel steps with no dependency → one plan file is fine
- Short tasks completable in one session → session log is sufficient

## Task Note Content Standards

Beyond the plan itself, task notes (and child task files) should record:

### Failure Documentation
When a run fails, append inline (do NOT save only to the session log):
- Failure artifact path (if produced)
- Root cause diagnosis (specific, not "it broke")
- Upstream files that need fixing
- Commands run to fix upstream
- Final rerun command and result (rows, columns, key stats)

Example structure:
```
- run result: FAILED — [specific error]
- failure artifact: results/[name]_conflicts.csv
- root cause: [diagnosis]
- fix: [upstream file] → [command]
- final rerun result: [N rows, M columns, 0 duplicate keys]
```

### Review Disposition
After any code review pass, append inline with severity tags in brackets:

```
- review pass [date] — [agent(s)]:
  - accepted and changed:
    - [critical] Added missing random.seed(42)
    - [major] Fixed hardcoded path on line 15
  - reviewed but left unchanged:
    - [minor] "Missing docstring on _helper()" — left: private function
```

Severity tags (`[critical]`, `[major]`, `[minor]`) are required — `review-tracker.py`
parses them into `quality_reports/review-hit-log.csv` for calibration.

Rationale: session logs record *sessions*; task notes record *tasks*. Failure and
review history belong to the task — they must survive context compression and be
readable by anyone picking up the task cold.
