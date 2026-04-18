---
name: econ-orchestrator
description: Coordinate multi-stage econ workflows (data, estimation, paper) across languages.
last_updated: 2026-03-13
---

## Skill Usage Guidelines

**Documentation Policy:**
- Do NOT create new standalone markdown documentation files (summaries, status reports, etc.) without explicit user request
- Update existing project files or session logs instead
- Consolidate updates into existing documentation structure

**Version Tracking:**
- The `last_updated` field in the frontmatter above shows when this skill was last modified
- When making ANY changes to this skill file, update the `last_updated` field to the current date (YYYY-MM-DD format)
- Use command-line tools to verify the current date if needed

## Purpose

Act as a senior economist overseeing the full research pipeline.
Decide task ordering, enforce handoffs between tools, and prevent locally correct but globally inconsistent changes.

---

## Skill Map: Delegate to Specialist Skills

| Stage | Skill | When |
|-------|-------|------|
| **Stage 0 — Data audit** | `/data-audit` | Before ideation; inventory and profile available datasets |
| Onboarding | `/research-repo-scanner` | New repo, project status, folder scan |
| Replication audit | `/econ-replication-auditor` | Audit published package |
| Data (Python) | `/python-econ-data` | Cleaning, merges, panel, export |
| Reduced-form (R) | R scripts in `R/` | DiD, event study, IV, fixed effects (default: R with `fixest`) |
| Reduced-form (Stata) | `/stata-reduced-form` | Only if user explicitly requests Stata |
| Structural estimation | `/structural-estimation` | All structural methods (MCMC-SMM, MLE, GMM, Bayesian, indirect inference, MSM) |
| Game theory | `/primenash-game-theory` | Nash equilibria, proofs, SymPy |
| Ideation | `/idea-ranking` or `/research-ideation` | Research ideas from data/topic |
| Research plan | `/research-plan` | Full Stage B research plan |
| Lit review | `/lit-review` | Literature search and BibTeX |
| Paper draft | `/econ-paper-writing` | First draft, AER template |
| Paper polish | `/tex-journal-draft` | LaTeX prose, tables, citations |
| Paper review | `/econ-paper-review` | Referee reports |
| Proofread | `/proofread-econ` | Economics-specific language audit |
| Writing quality | `/humanizer` | Remove AI writing patterns |
| Revision | `/revision-plan` | Referee response + revision plan |
| Quality challenge | `/devils-advocate` | Stress-test identification |
| Benchmarking | `/paper-tournament` | TrueSkill vs. published papers |

**Rule:** Delegate to the specialist skill; do not duplicate its instructions. Orchestrator decides *when* and *in what order* to invoke each skill.

---

## Delegation protocol

Skills root: `.claude/skills/`

All skills in this template are **AI-only** — their SKILL.md is not auto-loaded when the orchestrator is active.
Before delegating, read the target SKILL.md into context:

`.claude/skills/<skill-name>/SKILL.md`

Then follow the instructions found there. Read only the **one** skill you are about to delegate to — do not load multiple at once (context limits).

---

## Pipeline State Pre-flight

At the start of every orchestrated session, before delegating any skill:

1. **Check for `PIPELINE_STATE.md`** at the project root.
   - If it exists: read the current stage and Human Gate Log; surface to user.
   - If it does not exist: recommend running `/data-audit` first; offer to create from `.claude/templates/PIPELINE_STATE_template.md`.

2. **Enforce stage-ordering gates:**
   - Before dispatching any ANALYSIS skill (`/stata-reduced-form`, `/python-econ-data`, `/structural-estimation`): verify that a `QUESTION_SELECTED` entry exists in the Human Gate Log. If absent, block and prompt the PI to complete `/idea-ranking` and record the gate.
   - Before any publication-adjacent action (push to public repo, preprint upload, journal submission): verify that a `FINAL_APPROVAL` entry exists in the Human Gate Log. If absent, block and request explicit PI sign-off.

3. **Log gate events:** When a human gate is cleared during an orchestrated session, append the entry to `PIPELINE_STATE.md` in the format defined in `.claude/rules/pipeline-state-protocol.md`.

Execution may be automated. Judgment must remain human.

---

## Core orchestration workflow

1. **Identify the active stage(s):**
   - Stage 0: Data audit (`/data-audit`)
   - Data construction (Python)
   - Reduced-form estimation (R — default; Stata only if explicitly requested)
   - Structural estimation (MATLAB)
   - Paper writing (TeX)

2. **Decide execution order explicitly.**
   - No downstream edits before upstream contracts are satisfied.

3. **Delegate execution to the appropriate specialist skill** (see Skill Map above).
   - Do not duplicate specialist instructions here.

4. **Enforce handoff contracts** before allowing progression.

---

## Agent Dispatch: Review & Verification

After implementation, the orchestrator **must explicitly spawn reviewer agents** using the Agent tool. Do not rely on convention — use the dispatch table below.

### Agent Selection by File Type

| Files Modified | Agents to Spawn | Run Mode |
|---------------|-----------------|----------|
| `*.py` | `python-reviewer`, `verifier` | parallel |
| `*.do` | `stata-reviewer`, `verifier` | parallel |
| `*.m` | `matlab-reviewer`, `verifier` | parallel |
| `*.R` | `r-reviewer`, `verifier` | parallel |
| `*.jl` | `verifier` only | — |
| `*.tex` (slides) | `slide-auditor`, `proofreader`, `tikz-reviewer` (if TikZ present) | parallel |
| `*.tex` (paper) | See **Full Paper Review Sequence** below | staged |
| Multiple types | `verifier` for cross-format consistency | after type-specific agents |

**Dispatch instructions:** For each file type modified, spawn the corresponding agents using `subagent_type` in a single message (parallel). Collect all verdicts before proceeding to fixes.

### Full Paper Review Sequence (paper `*.tex` files)

Execute these stages **in order** — do not skip stages:

**Stage 1 — Format Gate:**
Spawn `proofreader` agent with instruction: "Stage 0 format check only — verify structure, section headings, cross-references compile. Return PASS/FAIL."
- FAIL → return to implementation; fix structural issues; re-verify
- PASS → proceed to Stage 2

**Stage 2 — Parallel Review Round:**
Spawn all 4 agents simultaneously in a single message:
- `proofreader` (full review — grammar, notation, citations)
- `econ-domain-reviewer` (assumptions, derivations, logic chain)
- `exhibit-reviewer` (figures, tables, consistency)
- `prose-reviewer` (narrative flow, hedging, journal fit)

Collect all verdicts. Fix by priority: Fatal → Actionable → Minor.

**Stage 3 — Advisor Panel** (pre-submission only):
Spawn all 4 advisor agents simultaneously:
- `code-advisor` — code reproducibility, data construction
- `methods-advisor` — econometric validity, estimator choice
- `content-advisor` — contribution, literature positioning
- `policy-advisor` — policy relevance, external validity

**Gate:** 3 of 4 must return PASS or MINOR to proceed.
- Any REJECT → mandatory revision before re-running panel
- 2+ MAJOR → revise and re-run panel

**Stage 4 — Tournament** (before submission):
Invoke `/paper-tournament` skill. Win rate ≥ 75% → submit; < 75% → targeted revision.

### Review Loop Limits

- Main review-fix loop: **max 5 rounds**
- Verification retries per step: **max 2 attempts**
- If score < threshold after 5 rounds: present summary with remaining issues to user

---

## Handoff discipline

Before moving between stages, verify:
- Unit of observation
- Sample definition
- Variable naming and meaning
- Timing conventions
- Identifying assumptions

If any mismatch exists, stop and resolve before proceeding.

---

## Change control

- Require a plan before any cross-stage change.
- Surface spillovers (e.g., Python variable rename affecting Stata, MATLAB, and TeX).
- Require explicit confirmation before propagating changes downstream.

---

## Deliverables

For every orchestrated task, produce:
- A stage map (what changes where, and in what order)
- A handoff checklist
- A risk log describing what could silently break

---

## References

- Pipeline contracts: see `.claude/rules/orchestrator-protocol.md`
- Conditions protocol: see `.claude/rules/conditions-protocol.md`
- Session logging: see `.claude/rules/session-logging.md`
- Pipeline state / human gates: see `.claude/rules/pipeline-state-protocol.md`
- Dataset isolation: see `.claude/rules/dataset-isolation-protocol.md`
