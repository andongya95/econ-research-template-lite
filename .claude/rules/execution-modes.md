---
paths: ["quality_reports/plans/**", "quality_reports/sessions/**"]
---

# Execution Modes: Shared Base Loop and Mode Overrides

---

## Base Loop (all modes)

Every plan step passes through this sequence:

```
IMPLEMENT → VERIFY → REVIEW → FIX → RE-VERIFY → SCORE
```

1. **IMPLEMENT** — Execute the plan step (write code, draft text, run analysis)
2. **VERIFY** — Run/compile and check outputs (max 2 retries on failure)
3. **REVIEW** — Dispatch reviewer agents by file type (tier from `review-tier.py`)
4. **FIX** — Apply fixes in priority order: critical → major → minor
5. **RE-VERIFY** — Confirm fixes compile/run cleanly (max 2 retries)
6. **SCORE** — Apply quality-gates rubric

If score < threshold after step 6, loop back to step 3 (max 5 review-fix rounds).

---

## Limits (apply to all modes)

| Limit | Value |
|-------|-------|
| Review-fix rounds per step | 5 |
| Verification retries | 2 |
| Never loop indefinitely | enforced |

---

## Mode Override Table

| Behavior | Standard | Autonomous | Team |
|----------|----------|------------|------|
| **Trigger** | (default) | "just do it" / "run autonomously" / "handle it" / "I'm going to sleep" | "team mode" / "run as a team" |
| **Pause between steps?** | Yes | Only at human gates | PI sync meeting between rounds |
| **Commit policy** | Only when user asks | Auto at score >= 80 | PI merges per round at >= 80 |
| **Logging** | Present summary to user | Session log only — no presentation | team-log.md + sync-meeting.md |
| **Agent dispatch** | Single agent + reviewers | Single agent + reviewers | Coauthors in waves + reviewers |
| **Human gates block?** | Yes | Yes | Yes |
| **On exhausted retries** | Present remaining issues | Log-and-skip to next step | PI logs, carries to next round |
| **Context limit** | User manages | Auto-continuation (see below) | PI saves handoff, continues |
| **Environment variable** | — | `CLAUDE_AUTONOMOUS_MODE=1` | combinable with autonomous |

---

## Human Gates (all modes, non-negotiable)

These gates **cannot** be auto-approved in any mode:

- **QUESTION_SELECTED** — PI chooses the research question
- **FINAL_APPROVAL** — PI approves publication

When a human gate is reached: save state, log progress, stop and request human input.

---

## Auto-Continuation (Autonomous + Team)

When context reaches ~85%, the agent does NOT stop. Instead:

1. Save a handoff file: `quality_reports/handoff.json`
   ```json
   {
     "plan": "quality_reports/plans/YYYY-MM-DD_description.md",
     "current_step": 5,
     "completed_steps": [1, 2, 3, 4],
     "skipped_steps": [],
     "key_decisions": ["chose CS-DiD over TWFE", "clustered at state level"],
     "session_log": "quality_reports/sessions/YYYY-MM-DD_autonomous.md",
     "git_head": "abc1234",
     "timestamp": "2026-03-30T02:15:00",
     "handoff_depth": 0
   }
   ```
2. Commit all progress
3. Spawn a fresh Claude session that reads the handoff and resumes:
   ```bash
   claude -p --dangerously-skip-permissions \
     "Continue from handoff at quality_reports/handoff.json. \
      Read the plan and resume from step N. Run autonomously."
   ```

This creates an infinite execution chain — each session picks up where the last left off. The only stops are human gates and budget limits.

**The `run-autonomous.sh` script handles this loop externally.**

### Interactive Sessions (no shell script)

In interactive sessions, auto-continuation uses **subagent delegation** instead of handoff files:

1. When context is high and implementation work remains, spawn Agent subagents for remaining steps
2. Each subagent gets fresh context and reads the plan from disk
3. The parent collects results and continues orchestrating
4. **Never tell the user to start a fresh session** — delegate to subagents instead

---

## Mode Selection Logic

1. Check trigger phrases (see override table)
2. If no trigger phrase → Standard mode
3. Autonomous and Team can combine (PI runs autonomously, coauthors as subagents)
4. "Just do it" is now part of Autonomous mode (same behavior)
