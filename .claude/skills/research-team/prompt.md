# /research-team — Multi-Coauthor Research Team

Initialize and run the multi-coauthor research team. Creates the team workspace, initializes
per-agent memory files, and launches the PI coordinator for the first round.

---

## Prerequisites

Before launching the team:
1. A research plan must exist in `quality_reports/plans/`
2. `PIPELINE_STATE.md` must show stage >= 2 (DATA_COLLECTION complete)
3. QUESTION_SELECTED gate must be logged (if in stage >= 3)

---

## Initialization Steps

### 1. Create workspace (if not exists)

```
quality_reports/team/
├── memory/
│   ├── pi-memory.md
│   ├── econometrician-memory.md
│   ├── paper-writer-memory.md
│   └── theorist-memory.md
└── team-log.md
```

### 2. Initialize memory files

For each coauthor, create their memory file if it doesn't exist:

```markdown
# {Role} Memory
**Last updated:** YYYY-MM-DD round 000 (initialized)

## Lessons
(none yet)

## Running Context
- Awaiting first assignment from PI
```

### 3. Initialize team log

```markdown
# Research Team Log
**Project:** [from CLAUDE.md]
**Initialized:** YYYY-MM-DD

## Rounds
(none yet — PI coordinator will begin Round 001)
```

### 4. Launch PI Coordinator

Spawn the `pi-coordinator` agent (see `.claude/agents/pi-coordinator.md`) with:
- Path to the approved research plan
- Current pipeline stage from `PIPELINE_STATE.md`
- Instruction to begin Round 001

---

## Usage

```
/research-team                            # Initialize and start round 1
/research-team resume                     # Resume from last completed round
/research-team round N                    # Start specific round N
/research-team status                     # Show current team status (reads state.json)
/research-team --max-rounds 5             # Limit to 5 rounds (default: 10)
/research-team --max-budget-usd 8.00      # Cap total agent spend
```

### Budget and Round Limits

The PI coordinator tracks cumulative cost and round count in
`quality_reports/team/state.json`. When either limit is reached, the PI saves
state and stops gracefully. Default max rounds: 10. Default budget: unlimited.

### Resume Mode

When resuming:
1. Read `quality_reports/team/team-log.md` for last completed round
2. Read the last `sync-meeting.md` for carried-over items
3. Launch PI coordinator to continue from the next round

### Status Mode

When checking status, read `quality_reports/team/state.json` and display:
1. Current round number and pipeline stage
2. Each agent's last score and status
3. Open REVISE/REJECT items (convergence status)
4. Budget spent vs. limit (if set)
