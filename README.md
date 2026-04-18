# Econ Research Template (Lite)

A lightweight AI-powered research workflow template for empirical economics, built for [Claude Code](https://docs.anthropic.com/en/docs/claude-code). This is the **lite** version — a strict subset of the full [econ-research-template](https://github.com/andongya95/econ-research-template) focused on the core multi-agent workflow without the heavy orchestration machinery.

**What you get:** 9 specialized agents (PI coordinator + 3 coauthors + verifier + autonomous-worker + 2 reviewers), 11 slash-command skills, 13 research rules, 13 lifecycle hooks, 4 protocol docs. ~84 files total vs ~195 in the full template.

**What's been dropped:** advisor panel, journal-review simulation, tournament benchmarking, structural estimation, theory-workflow, primenash-game-theory, literature-review automation, migration, all specialized reviewers beyond verifier/r/python, most proofreading and revision machinery. If you need these, use the full template.

The template operates in **contractor mode**: you direct the research, Claude orchestrates the execution. Two decision points always require human judgment — research question selection and publication approval. Everything else can run autonomously.

---

## Table of Contents

- [Quick Start](#quick-start)
- [What's in Lite](#whats-in-lite)
- [Execution Modes](#execution-modes)
- [Key Skills](#key-skills)
- [Memory System](#memory-system)
- [Quality Gates](#quality-gates)
- [Human Gates](#human-gates)
- [Upgrading to Full Template](#upgrading-to-full-template)

---

## Quick Start

### Prerequisites

- [Claude Code CLI](https://docs.anthropic.com/en/docs/claude-code) installed and authenticated
- Git repository initialized
- R 4.0+ and/or Python 3.10+

### Bootstrap a new project

```bash
# Clone the lite template
git clone https://github.com/Guojun-He-Research-Team/econ-research-template-lite my-project
cd my-project

# Create your project directories (no init script in lite)
mkdir -p data/{raw,processed} scripts R src paper literature \
         quality_reports/{plans,sessions,paps}

# Fill in CLAUDE.md with your project details
# (replace [PROJECT NAME], [Key question], [Identification], etc.)
$EDITOR CLAUDE.md
```

### First session

```bash
claude
```

Read `CLAUDE.md` when Claude Code opens. Start with `/research-plan` to draft a Stage B research plan, or `/workflow-help` for a visual overview.

---

## What's in Lite

### Agents (9)

Team + verifier + minimum reviewers. All the specialized referees, advisors, and secondary reviewers have been removed.

| Agent | Role |
|---|---|
| `pi-coordinator` | Orchestrates the research team, makes merge decisions, runs sync meetings |
| `econometrician` | Implements estimation code, runs robustness, produces tables |
| `paper-writer` | Drafts paper sections, manages exhibits, positions in literature |
| `theorist` | Derives models, propositions, proofs, theoretical predictions |
| `verifier` | Verifies code runs, outputs valid, tasks complete |
| `autonomous-worker` | Executes approved plans without stopping in autonomous mode |
| `_team-coauthor-base` | Shared base template for the 3 coauthor agents |
| `r-reviewer` | Reviews R scripts for quality, reproducibility, correctness |
| `python-reviewer` | Reviews Python scripts for quality, reproducibility, numerical correctness |

### Skills (11)

Core research pipeline + R + Python + writing.

| Skill | When to use |
|---|---|
| `/econ-orchestrator` | Coordinate multi-stage econ workflows across languages |
| `/research-team` | Run PI + econometrician + paper-writer + theorist in parallel |
| `/research-plan` | Draft a Stage B research plan (question, identification, specification, robustness, power) |
| `/analysis-spec` | Scaffold a regression spec-design note before coding |
| `/r-reduced-form` | R econometrics — DiD, event study, IV, FE, RDD (fixest, did, rdrobust, modelsummary) |
| `/r-econ-data` | R data cleaning, panel construction, merges, reshaping |
| `/python-econ-data` | Python data cleaning, panel construction, export for regression |
| `/econ-paper-writing` | Draft empirical econ papers for top journals |
| `/learn` | Record a lesson to MEMORY.md |
| `/context-status` | Show session health — context usage, active plan, preservation state |
| `/workflow-help` | Visual overview of pipeline stages, team structure, skill routing |

### Rules (12)

Always-loaded research-behavior directives.

- **Global:** r-default, plan-first-workflow, session-logging, pre-analysis-plan, verification-protocol, quality-gates, meta-governance
- **Path-scoped:** autonomous-mode, execution-modes, orchestrator-protocol, conditions-protocol, dataset-isolation-protocol

### Hooks (13)

Core lifecycle + team-mode memory isolation + autonomous-mode support.

- **Lifecycle:** `_utils.py`, `session-start-context.py`, `stop-checkpoint.py`, `pre-compact.py`, `post-compact-restore.py`
- **Quality:** `commit-logger.py`, `review-tier.py`, `verify-reminder.py`, `context-monitor.py`
- **Discipline:** `plan-path-guard.py`, `team-memory-isolation.py`, `sync-auto-memory.py`
- **Notifications:** `notify.sh`, `notify.ps1`

### Protocol docs (4)

Reference docs — not auto-loaded as rules, but available when you look them up.

- `autonomous-runbook.md` — 12 failure modes and recovery procedures for autonomous mode
- `research-team-protocol.md` — full team coordination protocol
- `orchestrator-research.md` — contractor mode execution loop
- `pipeline-state-protocol.md` — human gates and dataset lock

---

## Execution Modes

| Mode | Trigger | Use when |
|---|---|---|
| **Standard** | (default) | Interactive research, one task at a time |
| **Team mode** | "run as a team" / "team mode" | PI + 3 coauthors work in parallel rounds with sync meetings |
| **Autonomous** | "run autonomously" / "handle it" / "I'm going to sleep" | Long-running unattended execution — loops until the plan is done or a human gate is hit |

Team mode and autonomous mode can combine: PI runs autonomously, spawns coauthors as subagents.

**Autonomous mode runner:**
```bash
bash .claude/run-autonomous.sh quality_reports/plans/YYYY-MM-DD_description.md
```

---

## Key Skills

### Research-plan first
`/research-plan` — draft a Stage B plan. Defines the research question, identification strategy, specifications, robustness checks, and power calculations. Always do this before writing analysis code.

### Pre-analysis plan
The `pre-analysis-plan` rule (always loaded) enforces locking all empirical specifications before touching real data. Use `.claude/templates/pap-template.md` as a starting point. Save to `quality_reports/paps/YYYY-MM-DD_topic.md`, get sha256sum, commit with "Lock PAP" message, then write analysis code.

### Analysis
`/r-reduced-form` for econometrics — DiD (including Callaway-Sant'Anna), event studies, IV/2SLS, fixed effects with `fixest`, RDD with `rdrobust`, regression tables with `modelsummary`.

`/r-econ-data` and `/python-econ-data` for data cleaning and panel construction.

### Writing
`/econ-paper-writing` for drafting paper sections with top-journal conventions (identification language, coefficient translation, table formatting, citation workflow).

### Team mode
`/research-team` runs the full multi-coauthor team. PI coordinator assigns work to econometrician + paper-writer + theorist, they work in parallel, PI holds sync meetings to merge/revise.

---

## Memory System

- **`MEMORY.md`** — cross-session corrections and `[LEARN:category]` entries. Read at the start of every session. Append corrections as you discover them.
- **`quality_reports/memory/global.md`** — always-loaded global facts
- **`quality_reports/memory/stage-N-*.md`** — stage-scoped memory for each pipeline stage
- **`quality_reports/sessions/`** — session logs (why decisions were made)
- **`quality_reports/plans/`** — plans saved to disk, survive context compression

Use `/learn` to record a correction. Never delete old `[LEARN:]` entries.

---

## Quality Gates

Claude scores work against a rubric defined in `.claude/rules/quality-gates.md`.

| Score | Gate | Action |
|---|---|---|
| 80+ | Commit-ready | `git commit` allowed |
| 90+ | PR-ready | `gh pr create` |
| 95+ | Excellence | Aspirational |
| <80 | Blocked | Fix blocking issues before commit |

Paper `*.tex` files go through a **format gate** first (citation count ≥ 10, no placeholder text, all figures exist, no `???` references). Format gate failures block content scoring entirely.

---

## Human Gates

These two gates **cannot** be auto-approved in any mode, including autonomous:

- **`QUESTION_SELECTED`** — PI selects the research question. Recorded in `PIPELINE_STATE.md`.
- **`FINAL_APPROVAL`** — PI approves publication. Required before Stage 6 (Submission).

When autonomous mode hits a human gate: the runner saves state to `quality_reports/gates-pending.md`, logs progress, and stops. The user resolves the gate, then resumes.

---

## Upgrading to Full Template

If you find you need the things the lite template dropped — advisor panel pre-submission review, journal-review peer simulation, tournament benchmarking, structural estimation (SMM/MLE/GMM with JAX), theory workflow, literature automation, specialized language reviewers, proofreader — switch to the full template:

```
https://github.com/andongya95/econ-research-template
```

The full template is a superset: every file in lite exists in full, with the same paths and APIs. You can migrate a lite project to full by copying over your `quality_reports/`, `data/`, `paper/`, etc., into a fresh clone of the full template.

---

*Lite template. Built for research projects that want the PI coordinator, team mode, and autonomous mode without the heavier orchestration machinery of the full template.*
