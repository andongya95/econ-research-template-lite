# .claude/ Workflow Index — Lite

Quick-reference map of all skills, agents, rules, and docs in this lite template. For the full template (29 agents, 36 skills, 19 rules, 15 docs, advisor panel, journal review, tournament, structural estimation), see https://github.com/andongya95/econ-research-template.

**Architecture:** Single source of truth in root `.claude/`. Stage scoping via `stage-manifests.md`. Protocol docs in `.claude/docs/` (not auto-loaded as rules).

---

## Pipeline Stages → Skills → Agents

See `stage-manifests.md` for the per-stage breakdown (lite variant).

---

## Review Sequence (spawned by `/econ-orchestrator`)

### Code Review (by file type, after implementation)

| Files | Agents (parallel) |
|-------|-------------------|
| `*.py` | python-reviewer + verifier |
| `*.R` | r-reviewer + verifier |

Review depth determined by `python .claude/hooks/review-tier.py` (LIGHT/STANDARD/FULL).

**Note:** Lite only ships `python-reviewer`, `r-reviewer`, and `verifier`. For `*.do`, `*.m`, and `*.tex` reviewers (stata-reviewer, matlab-reviewer, slide-auditor, proofreader, tikz-reviewer, exhibit-reviewer, prose-reviewer, econ-domain-reviewer), use the full template.

**Paper Review (staged)** — not available in lite. The full template runs proofreader format gate → parallel review (proofreader + econ-domain-reviewer + exhibit-reviewer + prose-reviewer) → advisor-panel (3-of-4 gate) → tournament (≥75% win rate) → journal-review. In lite, paper review is PI-only.

---

## Skills and Agents

**9 agents:** pi-coordinator, econometrician, paper-writer, theorist, verifier, autonomous-worker, _team-coauthor-base, r-reviewer, python-reviewer

**11 skills:** econ-orchestrator, research-team, research-plan, analysis-spec, r-reduced-form, r-econ-data, python-econ-data, econ-paper-writing, learn, context-status, workflow-help

Full stage mapping: `stage-manifests.md`

---

## Rules (13)

### Rules (.claude/rules/) — Loaded by Claude Code

| Rule | Scope | Enforcement |
|------|-------|-------------|
| coding-principles | **global** | advisory |
| plan-first-workflow | **global** | advisory |
| r-default | **global** | advisory |
| session-logging | **global** | stop-checkpoint hook |
| autonomous-mode | path-scoped (plans, sessions) | enforced |
| execution-modes | path-scoped (plans, sessions) | enforced |
| meta-governance | path-scoped (memory files) | advisory |
| orchestrator-protocol | path-scoped (plans, sessions) | enforced |
| conditions-protocol | path-scoped (plans) | enforced |
| dataset-isolation-protocol | path-scoped (scripts, R) | advisory |
| pre-analysis-plan | path-scoped | advisory |
| quality-gates | path-scoped (code files) | enforced |
| verification-protocol | path-scoped (code files) | enforced |

---

## Docs (4) — Reference only, NOT auto-loaded

autonomous-runbook, orchestrator-research, pipeline-state-protocol, research-team-protocol

---

## Hooks (13)

| Hook | Event | Decision |
|------|-------|----------|
| plan-path-guard.py | PreToolUse (Write) | block |
| team-memory-isolation.py | PreToolUse (Read/Glob/Grep/Bash) | block |
| pre-compact.py | PreCompact | block |
| post-compact-restore.py | SessionStart | — |
| session-start-context.py | UserPromptSubmit | — |
| context-monitor.py | PostToolUse | approve (advisory) |
| verify-reminder.py | PostToolUse (Write/Edit) | approve (advisory) |
| commit-logger.py | PostToolUse (Bash) | — (silent) |
| stop-checkpoint.py | Stop | approve (advisory) |
| sync-auto-memory.py | Stop | — |
| review-tier.py | standalone script | called by orchestrator |
| notify.sh / notify.ps1 | Notification | — |
| _utils.py | (library — imported by other hooks) | — |
