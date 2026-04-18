# Stage Manifests — What Loads Per Stage (Lite)

The PI agent reads this file at stage transitions to determine which skills, agents, and rules are relevant. This is the **lite** variant — fewer skills/agents than the full template.

**How it works:** All definitions live in root `.claude/`. This manifest tells the orchestrator which to prefer per stage. Skills/agents not listed can still be used — this is guidance, not enforcement.

---

## Stage 0 — Discovery

**Skills:** (none in lite — PI handles question selection directly; full template has data-audit, idea-ranking, research-ideation)
**Agents:** (none — PI only)
**Rules:** (none path-scoped for this stage in lite)
**Memory:** quality_reports/memory/global.md + stage-0-discovery.md

*Note: QUESTION_SELECTED human gate must be resolved before leaving this stage.*

---

## Stage 1 — Planning

**Skills:** research-plan
**Agents:** (none)
**Rules:** conditions-protocol, pre-analysis-plan
**Memory:** global.md + stage-1-planning.md

*Note: Lite drops resolve-conditions skill and research-planning-protocol doc. Use research-plan only.*

---

## Stage 2 — Data

**Skills:** r-econ-data, python-econ-data
**Agents:** verifier (global), r-reviewer, python-reviewer
**Rules:** dataset-isolation-protocol
**Memory:** global.md + stage-2-data.md

---

## Stage 3 — Analysis

**Skills:** r-reduced-form, analysis-spec
**Agents:** econometrician, theorist
**Rules:** quality-gates, verification-protocol, r-default
**Memory:** global.md + stage-3-analysis.md

*Note: Lite drops stata-reduced-form, structural-estimation, theory-workflow, and primenash-game-theory. For those, use the full template.*

---

## Stage 4 — Writing

**Skills:** econ-paper-writing
**Agents:** paper-writer
**Rules:** (lite drops proofreading-protocol, literature-protocol, no-pause-beamer, tikz-visual-quality)
**Memory:** global.md + stage-4-writing.md

*Note: Lite drops tex-journal-draft, humanizer, proofread-econ, lit-review, literature-organize, citation-audit, and all specialized paper reviewers (proofreader, prose-reviewer, econ-domain-reviewer, exhibit-reviewer, slide-auditor, tikz-reviewer).*

---

## Stage 5 — Review

**Skills:** (none in lite — full template has advisor-panel, paper-tournament, journal-review, econ-paper-review, revision-plan, devils-advocate)
**Agents:** (none in lite — full template has code-advisor, methods-advisor, content-advisor, policy-advisor, tournament-judge, journal-editor, field-expert-referee, methods-referee, generalist-referee)
**Docs:** (none for review protocols in lite)
**Memory:** global.md + stage-5-review.md

*Note: FINAL_APPROVAL human gate must be resolved before leaving this stage. Since lite drops the advisor panel and journal review, pre-submission review is PI-only — consider upgrading to the full template if you want adversarial pre-submission review.*

---

## Stage 6 — Submission

**Skills:** (none in lite — full template has submission-checklist, econ-replication-auditor)
**Agents:** (none)
**Docs:** (none — replication-protocol not shipped in lite)
**Memory:** global.md + stage-6-submission.md

---

## Global (always available)

**Skills:** econ-orchestrator, research-team, learn, context-status, workflow-help
**Agents:** pi-coordinator, verifier, autonomous-worker
**Agents (base templates):** _team-coauthor-base
**Rules:** coding-principles, session-logging, plan-first-workflow, meta-governance
**Hooks:** all 13 hooks
