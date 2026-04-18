---
paths: ["scripts/run-autonomous.sh", "quality_reports/plans/**", "quality_reports/sessions/**"]
---

# Autonomous Mode: Continuous Long-Running Execution

Enables uninterrupted plan execution across multiple sessions. Merges the former "Just Do It" mode — there is now one autonomous mode for all unattended work.

---

## Trigger Phrases

Any of: "just do it", "handle it", "run autonomously", "I'm going to sleep", "handle everything", "run overnight", "don't stop", "execute the full plan"

---

## Core Rules

### 1. NEVER STOP to ask "should I continue?"

Loop until the plan is complete or a human gate is hit. Do not present intermediate summaries. Do not pause between steps. The user might be asleep.

### 2. Auto-commit at score >= 80

After each step completes the verify-review-fix loop:
- Score >= 80 → commit and advance
- Score < 80 after 5 rounds → log issues, commit with `[autonomous] partial:` prefix, advance

### 3. Log everything, present nothing

Write all decisions to `quality_reports/sessions/YYYY-MM-DD_description.md`. The session log is the record — not the conversation output.

### 4. Log-and-skip on exhausted retries

When a step fails after all retries:
1. Log failure with exact error message
2. Commit partial progress with `[autonomous] skipped:` prefix
3. Advance to next step
4. Never loop indefinitely

### 5. Human gates are sacred

QUESTION_SELECTED and FINAL_APPROVAL cannot be auto-approved. When reached:
1. Write `quality_reports/gates-pending.md` with: gate name, timestamp, what's needed to resolve
2. Save state, log progress, stop and explain what's needed
3. The notification hook will alert the user

See `.claude/docs/autonomous-runbook.md` for full failure recovery procedures.

### 6. Auto-continuation at context limit

When context reaches ~85%, stop any polling loops and do NOT stop working. Instead:
1. Write `quality_reports/handoff.json` with: plan path, current step, completed steps, key decisions, git HEAD
2. Commit all progress
3. The external `run-autonomous.sh` script detects the handoff and spawns a fresh session

This means the agent NEVER "stops gracefully" due to context — it hands off and the work continues.

### 7. Silent hooks

Set `CLAUDE_AUTONOMOUS_MODE=1`. Hooks switch to silent/log-only:
- `context-monitor.py`: advisory only, never blocks
- `stop-checkpoint.py`: writes snapshots silently
- `verify-reminder.py`: info-only

---

## Memory Access (Scoped)

1. Read `quality_reports/memory/global.md` (P1 entries only)
2. Read current stage memory file
3. Do NOT read other stage memory files or team coauthor memory

---

## CLI Usage

```bash
# Single session (may auto-continue via handoff)
bash scripts/run-autonomous.sh quality_reports/plans/YYYY-MM-DD_description.md

# With higher budget
bash scripts/run-autonomous.sh quality_reports/plans/YYYY-MM-DD_description.md 50.00
```

---

## Delegation Under Context Pressure

When context is high during autonomous or interactive execution:
- **Never** tell the user to start a fresh session
- **Spawn subagents** for remaining implementation work — each gets fresh context
- For batch tasks (e.g., create 9 test files): spawn 3 parallel Agent workers, each handling a subset
- Save the plan to disk first so subagents can read it independently

## WARNING: --dangerously-skip-permissions disables ALL hooks

The `run-autonomous.sh` script uses `--dangerously-skip-permissions` to avoid
interactive permission prompts during unattended execution. This flag **disables
all Claude Code hooks** — including safety hooks like `context-monitor.py`,
`stop-checkpoint.py`, and `verify-reminder.py`.

Consequences:
- No hook-based budget or context warnings will fire
- Dataset isolation hooks will NOT run (rely on agent rules instead)
- Pre-commit quality checks via hooks are skipped

Mitigations:
- The script enforces its own `MAX_SESSIONS` safety cap
- `--max-budget-usd` still applies at the CLI level
- Agent rules (this file, dataset-isolation-protocol, etc.) still govern behavior
- Always review `quality_reports/sessions/` logs after an autonomous run

**Do not use `--dangerously-skip-permissions` in interactive sessions.** It is
intended only for unattended autonomous execution where no human is available to
approve permission prompts.

## Safety

- Human gates block in all cases
- Dataset isolation still applies
- Budget cap via `--max-budget-usd`
- Worktree isolation recommended for subagents
