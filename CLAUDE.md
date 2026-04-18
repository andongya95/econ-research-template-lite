# [PROJECT NAME] — Claude Code Project Constitution (Lite)

**Project:** [Project Name]
**Institution:** [Your Institution]
**Status:** [Active research / Working paper / Published]
**Last updated:** [YYYY-MM-DD]

---

## Core Principles

1. **Plan first** — enter plan mode for any task touching >2 files or >30 min work
2. **Verify after** — compile/run and confirm output before reporting done
3. **Quality gates** — 80 to commit, 90 for PR, 95 for excellence
4. **LEARN tags** — append `[LEARN:category] note` to MEMORY.md for corrections
5. **Session logs** — log decisions, rationale, and deviations in `quality_reports/sessions/`
6. **Read MEMORY.md** at the start of every session
7. **Human judgment** — PI owns question selection and publication approval (see `PIPELINE_STATE.md`)

---

## Project Overview

[2-3 sentences describing the research question, identification strategy, main contribution.]

**Key question:** [One sentence]
**Identification:** [What variation is exploited?]
**Estimator:** [Main method — DiD, IV, FE, etc.]
**Data:** [Dataset name, time period, unit of observation]

---

## Folder Structure

```
[project-root]/
├── CLAUDE.md               # This file
├── MEMORY.md               # Cross-session corrections
├── PIPELINE_STATE.md       # Pipeline state + human gates
├── README.md               # Project overview
├── literature/             # BibTeX + reading notes
│   └── references.bib
├── quality_reports/
│   ├── memory/             # Stage-scoped memory files
│   ├── plans/              # Plans saved to disk (created on demand)
│   ├── sessions/           # Session logs (created on demand)
│   └── paps/               # Pre-analysis plans (created on demand)
├── scripts/                # Entry-point scripts
│   └── run-autonomous.sh   # Autonomous mode runner
└── .claude/                # Claude workflow (lite)
    ├── settings.json       # Hook wiring
    ├── rules/              # 13 research rules
    ├── agents/             # Team + verifier + reviewers (9)
    ├── skills/             # Core research skills (11)
    ├── docs/               # Protocol reference (4)
    └── hooks/              # Lifecycle hooks (13)
```

---

## Language Defaults

| Task | Language |
|------|----------|
| Econometric analysis | **R** (`fixest`, `did`, `rdrobust`, `modelsummary`) |
| Data cleaning | R or Python (whichever fits the source) |
| Paper | LaTeX |

Always use R for econometrics unless the user explicitly requests otherwise.

---

## Execution Modes

| Mode | Trigger | Use when |
|------|---------|----------|
| **Standard** | (default) | Interactive research, one task at a time |
| **Team mode** | "run as a team" / "team mode" | PI + econometrician + paper-writer + theorist in parallel rounds |
| **Autonomous** | "run autonomously" / "handle it" / "I'm going to sleep" | Long-running unattended execution |

Team and autonomous can combine: PI runs autonomously, coauthors as subagents.

**Human gates** (never auto-approved in any mode):
- `QUESTION_SELECTED` — PI selects the research question
- `FINAL_APPROVAL` — PI approves publication

---

## Key Skills

| Skill | When to use |
|-------|-------------|
| `/econ-orchestrator` | Coordinate full research pipeline |
| `/research-team` | Multi-coauthor team mode |
| `/research-plan` | Draft a Stage B research plan |
| `/analysis-spec` | Scaffold a regression spec-design note |
| `/r-reduced-form` | R econometrics: DiD, event study, IV, FE, RDD |
| `/r-econ-data` | R data cleaning, panel construction |
| `/python-econ-data` | Python data cleaning |
| `/econ-paper-writing` | Draft empirical econ paper sections |
| `/learn` | Record a correction to MEMORY.md |
| `/context-status` | Check session health |
| `/workflow-help` | Visual overview of pipeline + team mode |

---

## Key Commands

```bash
# R
Rscript R/01_[step].R

# Python
python scripts/01_[step].py

# LaTeX
latexmk -pdf paper/main.tex

# Autonomous mode
bash .claude/run-autonomous.sh quality_reports/plans/[plan].md
```

---

*Lite template. For the full template with advisor panel, journal review simulation, tournament benchmarking, structural estimation, and theory workflows, see the main `econ-research-template` repo.*
