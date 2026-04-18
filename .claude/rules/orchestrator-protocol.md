---
paths: ["quality_reports/plans/**", "quality_reports/sessions/**"]
---

# Orchestrator Protocol: Contractor Mode

After a plan is approved, the orchestrator takes over autonomously.

## Execution Loop

The orchestrator runs the **base loop** defined in `execution-modes.md`:
IMPLEMENT → VERIFY → REVIEW → FIX → RE-VERIFY → SCORE.

Mode-specific behavior (pause policy, commit policy, logging verbosity, retry handling)
is determined by the active execution mode — see the override table in `execution-modes.md`.

**Active modes:** Standard (default), Just Do It, Autonomous, Team.
For Autonomous details: `autonomous-mode.md`. For Team details: `research-team-protocol.md`.

## Review Depth Tiers

Determine review depth **mechanically** after IMPLEMENT, before dispatching reviewers:

```bash
python .claude/hooks/review-tier.py
```

This script analyzes `git diff` and returns a JSON tier. Use the tier to dispatch:

| Tier | Agents dispatched |
|---|---|
| **LIGHT** | verifier only |
| **STANDARD** | type-specific reviewer + verifier |
| **FULL** | all matching reviewers + verifier + econ-domain-reviewer |

Do not override the script's tier downward. You may escalate upward if you have reason to.

## Review Disposition (after FIX)

After acting on reviewer findings, append a review disposition block to the active
task note or plan file before RE-VERIFY:

```
- review pass [date] — [agent(s) run]:
  - accepted and changed:
    - [critical] Added missing random.seed(42)
    - [major] Fixed hardcoded path on line 15
  - reviewed but left unchanged:
    - [minor] "Missing docstring on _helper()" — left: private function
```

Severity tags in brackets are **required**: `[critical]`, `[major]`, `[minor]`. The
`review-tracker.py` hook parses these to build `quality_reports/review-hit-log.csv`
for calibration analysis (see `/review-calibration`).

Minimum requirement: every STANDARD or FULL review tier must produce a disposition
block. LIGHT tier (verifier only) is exempt.

## Agent Selection by File Type

| Files Modified | Agents to Run |
|---------------|---------------|
| `*.py` | python-reviewer, verifier |
| `*.do` | stata-reviewer, verifier |
| `*.m` | matlab-reviewer, verifier |
| `*.R` | r-reviewer, verifier |
| `*.jl` | verifier (no julia-reviewer yet — future feature) |
| `*.tex` (paper) | See paper review sequence below |
| `*.tex` (slides) | slide-auditor, tikz-reviewer (if TikZ), proofreader |
| `*.tex` + `*.qmd` | slide-auditor, proofreader (parity check) |
| Economics content | econ-domain-reviewer |
| Multiple types | verifier for cross-format consistency |

Independent agents run in parallel. econ-domain-reviewer runs after others (needs context).

**Full Paper Review Sequence (paper `*.tex` files):**

```
Step 1 — Proofreader Stage 0 (format gate)
  ↓ FAIL → return to IMPLEMENT; fix structural issues; re-verify
  ↓ PASS
Step 2 — Parallel review round [run all 4 simultaneously]:
  proofreader (full) + econ-domain-reviewer + exhibit-reviewer + prose-reviewer
  ↓ Collect verdicts; fix by priority (Fatal → Actionable)
Step 3 — Advisor Panel [run all 4 simultaneously]:
  code-advisor + methods-advisor + content-advisor + policy-advisor
  ↓ 3-of-4 PASS/MINOR gate
  ↓ FAIL → revision-protocol; re-run panel after fixes
  ↓ PASS
Step 4 — Tournament (optional, before submission):
  /paper-tournament vs. benchmark papers in quality_reports/tournament/benchmarks/
  ↓ Win rate ≥ 75% → proceed; < 75% → targeted revision
  ↓ PASS
Step 5 — Journal Review (final gate, before submission):
  /journal-review — adversarial external peer review simulation
  ↓ ACCEPT or MINOR_REVISION → ready to submit
  ↓ MAJOR_REVISION → /revision-plan with referee reports
  ↓ REJECT → major rework or different journal
```

- Never run econ-domain-reviewer on a paper that failed the format gate.
- Advisor panel (Step 3) runs only for final pre-submission review, not every commit.
- Tournament (Step 4) runs before journal submission and after major revisions.
- Journal review (Step 5) is the final adversarial gate — simulates real peer review.

---

## Team Mode

Team mode replaces the single-agent orchestrator with a multi-coauthor research team.
See `research-team-protocol.md` for the full protocol and `execution-modes.md` for how
Team mode differs from Standard/Autonomous on pause, commit, and logging policies.
