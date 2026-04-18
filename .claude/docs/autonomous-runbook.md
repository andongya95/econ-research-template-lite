# Autonomous Mode — Failure Runbook

Recovery procedures for failures during autonomous (`run-autonomous.sh`) or
"just do it" execution.

---

## Failure Modes

| # | Trigger Condition | Symptom | Automated Mitigation | Manual Recovery |
|---|-------------------|---------|---------------------|-----------------|
| 1 | **Invalid handoff.json** | Script exits with "Invalid handoff file" | Script deletes corrupt file and stops | Check `quality_reports/sessions/` for last log. Re-run with plan file. |
| 2 | **Handoff depth > 3** | Script exits with "Handoff depth exceeded" | Script logs error to `quality_reports/sessions/` and exits | Likely an infinite loop — the plan step is failing repeatedly. Read the session log, fix the blocking step manually, then re-run. |
| 3 | **Budget exhausted** | Claude CLI exits with budget error | Script treats as normal session end; checks for handoff | Increase `--max-budget-usd` or break the plan into smaller steps. Check `quality_reports/sessions/` for progress. |
| 4 | **Human gate reached** | Script stops; `quality_reports/gates-pending.md` written | Notification hook fires | Read `gates-pending.md`, make the decision, remove the entry, then re-run. |
| 5 | **Plan file missing** | Script exits with "Plan file not found" | Immediate exit | Check the path. Plans live in `quality_reports/plans/`. |
| 6 | **Plan not APPROVED** | Script warns or exits | Interactive: asks to confirm; non-interactive: exits | Set `status: APPROVED` in the plan frontmatter. |
| 7 | **Max sessions reached** | Script exits with safety-cap message | Stops after 20 sessions | Check progress — likely the plan is too large. Split into sub-plans. |
| 8 | **Git conflicts** | Commit fails in autonomous mode | Agent logs failure, skips step | Resolve conflicts manually: `git status`, fix conflicts, commit, re-run. |
| 9 | **Test failures** | Score < 80 after 5 rounds | Agent commits with `[autonomous] partial:` prefix, advances | Read the review report in session log. Fix the failing test. Re-run affected step. |
| 10 | **Stale handoff** | Script detects handoff mtime unchanged | Deletes stale file and stops | The session ended without writing a new handoff — work is done or stuck. Check session log. |
| 11 | **Context exhaustion without handoff** | Session ends abruptly | No automated recovery | Read `quality_reports/sessions/` and `git log --oneline -10`. Manually create a handoff or restart the plan. |
| 12 | **Dropbox sync conflict** | Git objects corrupted (empty files in `.git/objects/`) | None | Run `git fsck`, delete 0-byte files in `.git/objects/`, retry. See session log 2026-04-13 for precedent. |

---

## Interpreting Session Logs

After an autonomous run, check:

```bash
# Latest session log
ls -lt quality_reports/sessions/*.md | head -1

# Recent commits
git log --oneline -10

# Any pending gates
cat quality_reports/gates-pending.md 2>/dev/null

# Handoff state
cat quality_reports/handoff.json 2>/dev/null | python -m json.tool
```

## Handoff File Schema

```json
{
  "plan": "quality_reports/plans/YYYY-MM-DD_description.md",
  "current_step": 5,
  "completed_steps": [1, 2, 3, 4],
  "skipped_steps": [],
  "key_decisions": ["chose CS-DiD over TWFE"],
  "session_log": "quality_reports/sessions/YYYY-MM-DD_autonomous.md",
  "git_head": "abc1234",
  "timestamp": "2026-04-13T02:15:00",
  "handoff_depth": 1
}
```

Required keys: `plan`, `current_step`. All others are informational.
`handoff_depth` is incremented by `run-autonomous.sh` on each continuation.
If depth > 3, the script stops — this likely indicates an infinite loop.

## Recovery Checklist

1. Read the session log (why did it stop?)
2. Check `git log --oneline -10` (what was committed?)
3. Check `quality_reports/gates-pending.md` (any human decisions needed?)
4. Check `quality_reports/handoff.json` (can it be resumed?)
5. Fix the blocking issue
6. Re-run: `bash scripts/run-autonomous.sh <plan-file>`
