---
name: workflow-help
description: Visual overview of pipeline stages, team structure, skill routing. Use when onboarding.
allowed-tools: ["Read", "Glob"]
---

# /workflow-help — Visual Workflow Reference

Display a comprehensive visual reference of the entire research workflow. Read project
state to fill in the current status section.

## Instructions

1. Read `PIPELINE_STATE.md` (if it exists) for the current pipeline stage
2. Glob `quality_reports/plans/*.md` for the most recent active plan
3. Output the full reference below, filling in Section 6 with live data

## Output Template

Print the following sections verbatim, replacing only the `[dynamic]` placeholders in
Section 6 with actual values from the project.

---

### Section 1 — Pipeline Overview

```
Stage 0        Stage 1          Stage 2              Stage 3        Stage 4       Stage 5         Stage 6
DATA_AUDIT → QUESTIONING → DATA_COLLECTION → ANALYSIS → WRITING → REVIEW → FINAL_APPROVAL
/data-audit   /idea-ranking    conditions-protocol   /stata-...     /econ-paper   advisor panel   (human gate)
              🔴 QUESTION_     /research-plan        /python-...    /tex-journal  /paper-tournament
              SELECTED gate                          /structural-estimation        /journal-review
                  🔴 FINAL_APPROVAL
```

---

### Section 2 — Skill Router

```
"I need to..."                          → Use this skill
─────────────────────────────────────────────────────────
Start a new project                     → /data-audit → /idea-ranking → /research-plan
Find related papers                     → /lit-review
Write/revise the paper                  → /econ-paper-writing or /tex-journal-draft
Run estimation code                     → /stata-reduced-form, /python-econ-data, /structural-estimation
Check my paper before submission        → /econ-paper-review (quick) or /journal-review (full)
Get feedback on methodology             → /devils-advocate
Work with a coauthor team               → /research-team (launches PI + 3 coauthors + specialists)
Respond to referee reports              → /revision-plan
Benchmark against published papers      → /paper-tournament
Check session health                    → /context-status
Record a lesson                         → /learn
Scan an existing project                → /research-repo-scanner
Onboard existing project to template    → /migrate-project
See this help page                      → /workflow-help
```

---

### Section 3 — Team Mode Structure

```
                    ┌─────────────────┐
                    │  PI Coordinator  │
                    │  (orchestrates)  │
                    └───────┬─────────┘
              ┌─────────────┼─────────────┐
              ▼             ▼             ▼
    ┌─────────────┐ ┌─────────────┐ ┌─────────────┐   ┌ ─ ─ ─ ─ ─ ─ ┐
    │Econometrician│ │ Paper Writer │ │  Theorist   │    Specialist(s)
    │  Wave 1     │ │  Wave 2     │ │  Wave 2     │   │  (dynamic)  │
    │             │ │             │ │             │    Wave 1 or 2
    │ scripts/    │ │ paper/      │ │ paper/theory│   │ literature/  │
    │ stata/ R/   │ │ slides/     │ │ src/model   │    (domain)
    │ results/    │ │ literature/ │ │ literature/ │   └ ─ ─ ─ ─ ─ ─ ┘
    │ literature/ │ │             │ │             │
    │  methods/   │ │             │ │             │
    └─────────────┘ └─────────────┘ └─────────────┘
         │                │               │
         └────────────────┼───────────────┘
                          ▼
                    Sync Meeting
                  MERGE / REVISE / REJECT
```

All coauthors have WebSearch + WebFetch for inline literature searches (3-5 papers).
Broader reviews → PI assigns `/lit-review`. Specialists are created on-the-fly by the PI.

---

### Section 4 — Literature Vault Quick Reference

```
literature/
├── references.bib     ← canonical BibTeX (append-only in team mode)
├── papers/            ← one note per paper ({author}{year}_{keyword}.md)
│   └── _template.md   ← copy this for new papers
├── topics/            ← thematic overviews (link to paper notes)
└── methods/           ← estimator/technique notes

Relevance: 1=tangential  2=related  3=important  4=key predecessor  5=direct competitor
Status:    unread → reading → read → cited

Team write access:
  Econometrician → methods/, papers/ (method-tagged)
  Paper Writer   → papers/ (empirical/policy), topics/
  Theorist       → papers/ (theory/mechanism), topics/
  Specialist     → PI-assigned per domain
```

---

### Section 5 — Quality Gates

```
Score    Meaning         Action
─────    ──────────      ─────────────────
95+      Excellence      Aspirational target
90+      PR-ready        gh pr create
80+      Commit-ready    git commit allowed
<80      Blocked         Fix issues first

Deductions: broken code (−100), NaN/Inf (−30), wrong SE clustering (−20),
            missing seed (−10), hardcoded paths (−20), unresolved citations (−15)
```

---

### Section 6 — Current Project State

Read from project files and fill in:

```
Current stage: [read from PIPELINE_STATE.md → Current Stage, or "not initialized"]
Active plan:   [most recent .md in quality_reports/plans/, or "none"]
Human gates:   [QUESTION_SELECTED: logged/pending] [FINAL_APPROVAL: logged/pending]
```
