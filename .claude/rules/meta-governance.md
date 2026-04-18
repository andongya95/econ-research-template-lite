---
paths: ["MEMORY.md", "quality_reports/memory/**"]
---

# Meta-Governance: Stage-Scoped Memory System

## Memory Architecture

| Location | Purpose | Committed? | When loaded |
|----------|---------|-----------|-------------|
| `quality_reports/memory/global.md` | P1 entries, cross-stage conventions | **Yes** | Always |
| `quality_reports/memory/stage-N-*.md` | Stage-specific lessons | **Yes** | When PI enters that stage |
| `quality_reports/memory/short-term.md` | Rolling 10-entry event log (FIFO) | **No** (gitignored) | Last 5 always at session start |
| `personal-memory.md` | Machine-specific paths, credentials | **No** (gitignored) | Always (local only) |
| `MEMORY.md` | Index file pointing to memory files | **Yes** | Reference only |

## At Session Start

1. Read `quality_reports/memory/global.md` (always)
2. Check `PIPELINE_STATE.md` for current stage
3. Read `quality_reports/memory/stage-N-*.md` for that stage
4. Read `personal-memory.md` if it exists

## Writing New Entries

- **P1 entries** (critical, cross-stage) → write to `global.md`
- **Stage-specific entries** → write to the current stage's memory file
- **Evaluator corrections** → write to current stage memory (reviewer calibration is contextual)
- **Machine-specific** → write to `personal-memory.md`

## Stage Transitions (PI Agent)

When moving from Stage N to Stage N+1:
1. Read stage-N memory file
2. Auto-tag entries as `[CARRY-FORWARD]` based on:
   - All P1 → always carry
   - P2 about conventions/notation → carry to writing stages+
   - P2 about estimation specifics → carry if next stage uses them
   - P3 → leave unless directly relevant
3. Copy `[CARRY-FORWARD]` entries to stage-(N+1) memory file
4. Report: what carried, what left behind

## Short-Term Memory (Automatic)

`quality_reports/memory/short-term.md` captures recent session events, not lessons.
Auto-written by `stop-checkpoint.py`; injected at session start as `## Recent Context`.

Captured automatically: git commits, plan task changes.
Pruned: FIFO-only, max 10 entries. No age-based pruning (shallow window flushes naturally).
Never edit manually. For lessons → use `/learn` → `global.md`.

## Safety Rules

1. **Never delete** — entries move between files, never disappear
2. **Git tracks everything** — `git log quality_reports/memory/` shows full history
3. **Human can edit** any memory file at any time
4. **Archive on completion** — merge all stage memories into `quality_reports/memory/archive/YYYY-MM-DD_[project].md`
