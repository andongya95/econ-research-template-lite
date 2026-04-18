# Global Memory — Always Loaded

Cross-stage facts and critical lessons. Loaded in every session regardless of pipeline stage.

**Entry format:** `[LEARN:category|P#|YYYY-MM-DD] lesson text`
**Carry-forward tag:** `[CARRY-FORWARD]` — PI adds this to entries that should migrate to next stage

---

## Critical (P1) — Never Skip

[LEARN:workflow|P1|2026-02-24] Plans survive context compression only if saved to `quality_reports/plans/`. Always save before implementation begins.

[LEARN:workflow|P1|2026-02-24] After context compaction: read CLAUDE.md + most recent plan + `git log --oneline -5` to re-orient.

## Cross-Stage Conventions (P2)

[LEARN:workflow|P2|2026-02-24] Session logs capture WHY decisions were made — git commits record WHAT changed. Both are needed.

[LEARN:workflow|P2|2026-02-26] Plans belong in `quality_reports/plans/`, NOT `quality_reports/sessions/`. The `plan-path-guard` hook enforces this.

[LEARN:workflow|P2|2026-02-26] Research workflow sequence: ideation → research plan → conditions → implement → review → advisor panel → tournament.

[LEARN:workflow|P2|2026-03-27] Harness principle: every rule/agent/hook encodes an assumption about what the model can't do. Periodically stress-test by removing components.

[LEARN:workflow|P2|2026-03-27] Plans require `### Success Criteria` per step before APPROVED. plan-path-guard.py enforces this.

[LEARN:workflow|P2|2026-03-27] Review depth determined by `python .claude/hooks/review-tier.py` (git diff → LIGHT/STANDARD/FULL). Do not override downward.

## Infrastructure (P3) — Load on Demand

[LEARN:workflow|P3|2026-02-26] On Windows, use `command -v python || command -v python3` (python first) in hook commands with Anaconda.

[LEARN:workflow|P3|2026-02-26] Session state files: `~/.claude/sessions/{project-hash}/`. Key files: `last-session-summary.json`, `pre-compact-state.json`, `context-monitor-cache.json`.

[LEARN:workflow|P3|2026-02-26] Pre-compact hook uses "block" decision — intentional, not an error.

[LEARN:workflow|P3|2026-03-13] `protect-files.sh` matches on path suffix, not basename.

[LEARN:workflow|P3|2026-03-03] Terminology: removed all 'APE' and 'HLER' branded labels. Rule: pipeline-state-protocol.md.

[LEARN:workflow|P2|2026-03-27] evaluator-context.py hook fires on SubagentStart. Reads subagent_type at top level, not nested tool_input.
