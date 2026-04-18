---
paths: ["quality_reports/team/**"]
---

# Research Team Protocol: Multi-Coauthor Agent Team

Replicates how a real economics research team works: multiple coauthors with distinct
roles working in parallel, with periodic sync meetings where the PI reviews progress,
coauthors discuss validity, and the PI decides what makes it into the main paper.

---

## The Core Team + Specialists

| Role | Agent | Responsibility | Scope |
|------|-------|----------------|-------|
| **PI / Domain Expert** | `pi-coordinator` | Orchestrates rounds, assigns tasks, runs sync meetings, makes keep/discard decisions | All project files |
| **Econometrician** | `econometrician` | Estimation, robustness, tables, pre-trend tests | `scripts/`, `stata/`, `R/`, `results/`, `data/processed/`, `literature/methods/` |
| **Paper Writer** | `paper-writer` | Drafts sections, exhibit layout, framing, lit positioning | `paper/`, `slides/`, `literature/` |
| **Theorist** | `theorist` | Model derivation, propositions, proofs, theoretical predictions, theory lit | `paper/` (theory), `src/` (model code), `literature/` |
| **Specialist (0-N)** | (created by PI) | Domain-specific expertise (history, health, political economy, etc.) | Defined at creation by PI |

Specialists are created dynamically by the PI when the core team lacks domain coverage.
See `pi-coordinator.md → Dynamic Specialist Dispatch` for the creation protocol.

---

## Trigger Phrases

Activate team mode when the user says any of:
- "run as a team"
- "coauthor mode"
- "launch the research team"
- "team mode"
- `/research-team`

---

## Workspace Structure

```
quality_reports/team/
├── round-NNN/                    # One folder per research round (3-digit, zero-padded)
│   ├── assignments.md            # PI's task assignments for this round
│   ├── econometrician-output.md  # Econometrician's deliverables + notes
│   ├── paper-writer-output.md    # Writer's deliverables + notes
│   ├── theorist-output.md        # Theorist's deliverables + notes
│   ├── {specialist}-output.md    # Specialist outputs (0-N, created as needed)
│   └── sync-meeting.md           # PI's review: decisions on each output
├── memory/                       # Per-agent persistent memory (isolated)
│   ├── pi-memory.md
│   ├── econometrician-memory.md
│   ├── paper-writer-memory.md
│   ├── theorist-memory.md
│   └── {specialist}-memory.md    # Specialist memory (auto-detected by hook)
└── team-log.md                   # Running log of all rounds + decisions
```

---

## Memory Isolation Rules (Critical)

Each coauthor agent:
1. Reads ONLY its own memory file (`quality_reports/team/memory/{role}-memory.md`)
2. Reads the shared research plan and PI assignments for the current round
3. Does **NOT** read other coauthors' memory files
4. Updates its own memory at the end of each round with lessons learned

The PI agent reads ALL outputs and ALL memories (coordinator privilege).

**Why isolation matters:** Prevents coauthors from anchoring on each other's reasoning.
The econometrician should form independent conclusions about the data without being
influenced by how the writer framed a result, and vice versa. Contradictions between
coauthors are valuable signals — they surface at sync meetings.

---

## The Round Loop

```
PI reads current state (plan, results, paper draft)
  │
  PI writes assignments.md for round N
  │  "Econometrician: run event study with 3 pre-periods"
  │  "Writer: draft identification strategy section"
  │  "Theorist: derive comparative statics for Proposition 1"
  │
  ┌──────────────────────────────────────────────┐
  │  PARALLEL EXECUTION (up to 3 agents)         │
  │                                               │
  │  Econometrician    Writer         Theorist    │
  │  reads assignment  reads assign.  reads assign│
  │  reads own memory  reads own mem  reads own m │
  │  implements        drafts         derives     │
  │  self-checks       self-checks    self-checks │
  │  writes output.md  writes out.md  writes out  │
  │  updates own mem   updates own m  updates own │
  └──────────────────────────────────────────────┘
  │
  PI reads ALL outputs
  │
  PI DISPATCHES REVIEWER AGENTS on merged work:
  │  - python-reviewer / stata-reviewer for code files
  │  - proofreader / prose-reviewer for .tex files
  │  - econ-domain-reviewer for economics content
  │  (Coauthors only do lightweight self-checks;
  │   formal review is centralized here at the PI level)
  │
  SYNC MEETING (PI evaluates reviewer findings + own assessment):
  │  - Are econometrician's results consistent with theory?
  │  - Does the writer's framing match the actual estimates?
  │  - Does the theory predict the sign/magnitude found?
  │  - Any contradictions between coauthors' work?
  │  - What did reviewer agents flag?
  │
  PI writes sync-meeting.md with decisions:
  │  MERGE:   "Event study looks clean — merge to main"
  │  REVISE:  "Writer's intro oversells — tone down claim"
  │  REJECT:  "Robustness spec 3 has wrong clustering — redo"
  │  DISCUSS: "Theory predicts positive but estimate is negative"
  │
  PI merges approved work to main branch
  │
  Next round (or DONE if all plan steps complete)
```

---

## File Ownership and Merge Conflict Prevention

Each coauthor has exclusive write access to specific directories per round. If two
coauthors need to edit the same file (e.g., both writer and theorist editing
`paper/main.tex`), the PI must assign ownership for that round.

| Directory | Default Owner | Override requires |
|-----------|--------------|-------------------|
| `scripts/`, `stata/`, `R/`, `results/` | Econometrician | PI assignment |
| `paper/` (empirical sections) | Paper Writer | PI assignment |
| `paper/` (theory sections, appendix) | Theorist | PI assignment |
| `src/` (model code) | Theorist | PI assignment |
| `slides/` | Paper Writer | PI assignment |
| `literature/` | Shared (append-only BibTeX) | — |
| Specialist directories | Specialist (PI-assigned per round) | PI assignment |

**Conflict resolution:** If a merge conflict occurs despite ownership rules:
1. PI keeps the version from the file's designated owner for that round
2. The other coauthor's changes become a REVISE task in the next round
3. PI may manually merge non-conflicting hunks if straightforward

**Git tagging for rollback:** After each round's merge, PI tags the commit:
`git tag team-round-NNN-{role}` for each merged coauthor branch. Enables
rollback via `git revert` if a later round reveals problems with merged work.

---

## Execution Order Within a Round

To prevent conflicts, coauthors execute in two waves:

1. **Wave 1 — Econometrician** (runs first, produces results)
   - Runs in worktree isolation
   - PI merges econometrician's branch after review

2. **Wave 2 — Writer + Theorist** (run in parallel, after econometrician merge)
   - Both run in worktree isolation
   - Can reference merged results from Wave 1
   - PI merges both branches after review

This ensures the writer and theorist always work with the latest estimation results.

**Exception:** If the econometrician has no tasks in a round (e.g., pure writing round),
all coauthors run in Wave 1 simultaneously.

**Specialists:** The PI assigns specialists to Wave 1 or Wave 2 based on task dependencies.
If a specialist needs estimation results → Wave 2. If independent → Wave 1 (parallel with
econometrician or other specialists).

---

## Sync Meeting Decisions

| Decision | Meaning | Next Action |
|----------|---------|-------------|
| **MERGE** | Output is correct and ready | PI merges the coauthor's branch |
| **REVISE** | Partially correct; needs specific changes | Coauthor gets revision task in next round |
| **REJECT** | Output is wrong or unusable | Coauthor redoes from scratch in next round |
| **DISCUSS** | Contradiction detected between coauthors | PI assigns reconciliation tasks to relevant coauthors |

---

## Coauthor Disagreement Protocol

Coauthors may flag disagreement with PI directives in their output reports:

```markdown
## Disagreement Flag
**PI asked:** cluster at state level
**My recommendation:** firm-level clustering is more appropriate because [reason]
**Evidence:** [specific reference to data structure or econometric principle]
```

The PI evaluates disagreements at the sync meeting:
- If the coauthor's reasoning is correct → PI adopts the change and logs it
- If the PI's original directive was correct → PI explains why and the coauthor proceeds
- If genuinely ambiguous → PI escalates to the human PI (real user)

---

## Convergence and Termination

| Condition | Action |
|-----------|--------|
| No REVISE or REJECT items in sync meeting | Stage complete — advance to next pipeline stage |
| Max 10 rounds per pipeline stage | Force-close — PI logs remaining issues, presents to user |
| Human gate reached (QUESTION_SELECTED, FINAL_APPROVAL) | Stop — save state, request human input |
| Context approaching limit (95%+) | Save all state, commit progress, stop gracefully |

---

## Quality Scoring

The PI applies quality gates at each sync meeting using the **base loop** scoring from
`execution-modes.md`. Team-specific thresholds:
- Score >= 80 per coauthor output → MERGE
- Score < 80 → REVISE (with specific feedback)
- Score < 50 → REJECT (fundamental issue)

Overall round score = min(individual coauthor scores). The round passes only when all
merged outputs score >= 80. See `execution-modes.md` for how Team mode overrides
compare to Standard/Autonomous on pause, commit, and logging policies.

---

## Integration with Existing Infrastructure

| Component | Integration |
|-----------|-------------|
| **Autonomous mode** | PI-coordinator runs in autonomous mode; coauthors are parallel subagents |
| **Pipeline stages** | Team operates within stages 3-5 (ANALYSIS → WRITING → REVIEW). Human gates still apply |
| **Session logging** | `team-log.md` is the master log; per-round `sync-meeting.md` files are detailed records |
| **MEMORY.md** | Project-level MEMORY.md still exists. Team memory files are working memory within the research process |
| **Orchestrator** | PI-coordinator replaces the generic orchestrator in team mode. Same quality gates |
| **Reviewer agents** | PI dispatches reviewer agents at sync meeting. Coauthors run lightweight self-checks only |
| **Worktree isolation** | Each coauthor gets an isolated git worktree via `isolation: worktree` |

---

## Per-Agent Memory Format

```markdown
# {Role} Memory
**Last updated:** YYYY-MM-DD round NNN

## Lessons
- [LEARN:category] Lesson learned from this project
- [LEARN:category] Another lesson

## Running Context
- Current specification: [what we're running]
- Key concern from PI: [latest feedback]
- My next priority: [what I plan to focus on]
```

---

## Round Folder Format

### `assignments.md`
```markdown
# Round NNN Assignments
**Date:** YYYY-MM-DD
**Pipeline stage:** [ANALYSIS / WRITING / REVIEW]

## Econometrician
- [ ] Task 1: [specific, actionable instruction]
- [ ] Task 2: [specific, actionable instruction]

## Paper Writer
- [ ] Task 1: [specific, actionable instruction]

## Theorist
- [ ] Task 1: [specific, actionable instruction]
```

### `{role}-output.md`
```markdown
# {Role} Output — Round NNN
**Date:** YYYY-MM-DD

## Completed Tasks
### Task 1: [title]
**Status:** DONE / PARTIAL / BLOCKED
**Files modified:** [list]
**Self-check score:** [N]/100
**Notes:** [key decisions, issues encountered]

## Disagreement Flags (if any)
[see disagreement protocol above]

## Memory Update
[Lessons learned this round — will be appended to own memory file]
```

### `sync-meeting.md`
```markdown
# Sync Meeting — Round NNN
**Date:** YYYY-MM-DD
**PI assessment:**

## Econometrician Output
**Decision:** MERGE / REVISE / REJECT / DISCUSS
**Score:** [N]/100
**Feedback:** [specific, actionable]

## Paper Writer Output
**Decision:** MERGE / REVISE / REJECT / DISCUSS
**Score:** [N]/100
**Feedback:** [specific, actionable]

## Theorist Output
**Decision:** MERGE / REVISE / REJECT / DISCUSS
**Score:** [N]/100
**Feedback:** [specific, actionable]

## Reviewer Agent Findings
[Summary of issues flagged by reviewer agents dispatched on merged work]

## Literature Vault Review
| Citekey | Added by | Domain | Action |
|---------|---------|--------|--------|

Cross-coauthor recommendations → route as tasks in next round.
Duplicate BibTeX keys → keep entry with more complete metadata.

## Cross-Coauthor Consistency
[Any contradictions detected? Reconciliation needed?]

## Merged to Main
- [list of files/branches merged]

## Carried to Next Round
- [REVISE/REJECT items become next round's assignments]
```
