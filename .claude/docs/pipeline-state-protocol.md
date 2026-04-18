---
paths: ["PIPELINE_STATE.md"]
---

# Pipeline State Protocol

Implements the human-in-the-loop research principles:
**Execution may be automated. Judgment must remain human.**

`PIPELINE_STATE.md` is the single RunState object per paper/project. Skills write to it;
the `econ-orchestrator` reads it to enforce stage ordering and gate compliance.

---

## The 7 Pipeline Stages

| Stage | Name | Skill(s) | Gate |
|-------|------|----------|------|
| 0 | DATA_AUDIT | `/data-audit` | — |
| 1 | QUESTIONING | `/idea-ranking` | 🔴 QUESTION_SELECTED |
| 2 | DATA_COLLECTION | `conditions-protocol` + `/research-plan` | — |
| 3 | ANALYSIS | `/stata-reduced-form`, `/python-econ-data`, `/structural-estimation` | — |
| 4 | WRITING | `/econ-paper-writing`, `/tex-journal-draft` | — |
| 5 | REVIEW | advisor panel + tournament | — |
| 6 | FINAL_APPROVAL | — | 🔴 FINAL_APPROVAL |

---

## Stage Transition Rules

1. **DATA_AUDIT must precede QUESTIONING** when data is available locally. If skipped, `/idea-ranking` issues a warning.
2. **QUESTION_SELECTED gate must be logged** before DATA_COLLECTION begins. The orchestrator does not advance past QUESTIONING without this entry.
3. **DATA_COLLECTION must complete** (all 5 conditions RESOLVED) before ANALYSIS begins.
4. **FINAL_APPROVAL gate must be logged** before any publication action (push to public repo, preprint upload, journal submission).

Stages may be re-entered (e.g., revised analysis after REVIEW). Re-entry is logged in PIPELINE_STATE with a timestamp and reason.

---

## `PIPELINE_STATE.md` Format

```markdown
# PIPELINE_STATE
**Paper ID:** [short slug, e.g., wages-automation-2026]
**PI:** [name]
**Institution:** [institution]
**Last updated:** YYYY-MM-DD

---

## Current Stage
**Stage:** [DATA_AUDIT | QUESTIONING | DATA_COLLECTION | ANALYSIS | WRITING | REVIEW | FINAL_APPROVAL]
**Status:** [IN_PROGRESS | COMPLETE | BLOCKED]
**Blocking reason:** [if BLOCKED]

---

## Active Dataset Lock
**Locked dataset(s):** [path(s) — set after DATA_COLLECTION begins]
**Locked on:** YYYY-MM-DD
**Cross-dataset joins:** [NONE | see unlock log below]

---

## Human Gate Log
<!-- Every human decision must be recorded here with name + timestamp. -->

### [YYYY-MM-DD HH:MM] QUESTION_SELECTED
**PI:** [name]
**Selected idea:** [title]
**Alternatives considered:** [brief list]
**Rationale:** [1-2 sentences]

### [YYYY-MM-DD HH:MM] FINAL_APPROVAL
**PI:** [name]
**Paper version:** [e.g., v2 / R1]
**Target venue:** [journal / preprint / working paper series]
**Statement:** "I approve this paper for submission/publication as described above."

---

## Dataset Unlock Log
<!-- Required for any cross-domain join after DATA_COLLECTION is complete. -->

### [YYYY-MM-DD HH:MM] DATASET_UNLOCK
**Authorized by:** [PI name]
**Datasets joined:** [list]
**Justification:** [why cross-join is valid — not spurious]

---

## Stage History
| Stage | Entered | Completed | Notes |
|-------|---------|-----------|-------|
| DATA_AUDIT | YYYY-MM-DD | YYYY-MM-DD | |
| QUESTIONING | YYYY-MM-DD | YYYY-MM-DD | |
| DATA_COLLECTION | YYYY-MM-DD | YYYY-MM-DD | |
| ANALYSIS | YYYY-MM-DD | YYYY-MM-DD | |
| WRITING | YYYY-MM-DD | YYYY-MM-DD | |
| REVIEW | YYYY-MM-DD | YYYY-MM-DD | |
| FINAL_APPROVAL | YYYY-MM-DD | — | |
```

---

## Authorship Accountability

The `PIPELINE_STATE.md` serves as the authoritative record of:
- Which human PI selected the research question (QUESTION_SELECTED gate)
- Which human PI authorized publication (FINAL_APPROVAL gate)
- What datasets were used and whether cross-joins were explicitly authorized

This record must be committed to version control before any submission.

---

## Orchestrator Responsibilities

When `econ-orchestrator` is invoked:
1. Check whether `PIPELINE_STATE.md` exists at project root
2. If it exists: read current stage and gate log; surface to user
3. If it does not exist: recommend running `/data-audit` first; offer to create from template
4. Before dispatching any ANALYSIS skill: verify QUESTION_SELECTED gate is logged
5. Before any publication action: verify FINAL_APPROVAL gate is logged; block if absent

---

## Setup

Copy `.claude/templates/PIPELINE_STATE_template.md` to `PIPELINE_STATE.md` at project root when
starting a new paper. The `/data-audit` skill will populate stage 0 automatically.
