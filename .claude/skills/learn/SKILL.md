---
name: learn
description: Record a lesson to MEMORY.md, or promote a multi-step lesson to a reusable skill
user_invocable: true
args: "[--as-skill name] [category] [text]"
---

# /learn — Record and Promote Lessons

## Default Mode: `/learn [category] [text]`

Append a prioritized, dated `[LEARN:category|P#|date]` entry to the project-root `MEMORY.md`.

### Entry Format

```
[LEARN:category|P#|YYYY-MM-DD] lesson text
```

**Priority levels:**
- `P1` — Critical. Always loaded regardless of context pressure. Use for lessons that prevent data loss, broken pipelines, or wrong results.
- `P2` — Important. Loaded when context < 80%. Use for workflow patterns, conventions, and recurring gotchas.
- `P3` — Reference. Loaded only on demand when the topic is relevant. Use for historical facts, one-time fixes, and edge-case notes.

### Steps

1. **Validate category** — valid categories: `workflow`, `data`, `estimation`, `model`, `stata`, `python`, `r`, `matlab`, `latex`, `slides`, `citation`, `evaluator`
2. **Assign priority** — if the user didn't specify, infer from the lesson:
   - Prevents data loss or wrong results → P1
   - Workflow pattern or recurring convention → P2
   - Historical note or edge case → P3
   - When uncertain, default to P2. Ask the user if the choice is ambiguous.
3. **Determine target file** — memory is split by stage:
   - P1 entries → `quality_reports/memory/global.md` (always loaded)
   - Stage-specific entries → `quality_reports/memory/stage-N-name.md` based on current pipeline stage
   - Check `PIPELINE_STATE.md` for current stage, or ask the user
   - Evaluator entries → current stage memory file (reviewer corrections are stage-contextual)
4. **Check for duplicates** — read the target memory file and check if a similar lesson exists. If so, update with `[UPDATED YYYY-MM-DD: ...]`.
5. **Append** — add `[LEARN:category|P#|YYYY-MM-DD]` text to the target memory file. Use today's date.
6. **Confirm** — show the user: what was added, which file, which priority, and why.

### Examples

```
/learn workflow Always run latexmk twice after changing references
→ [LEARN:workflow|P2|2026-03-27] Always run latexmk twice after changing references

/learn estimation The optimizer diverges when rho > 2.5 — add upper bound
→ [LEARN:estimation|P1|2026-03-27] The optimizer diverges when rho > 2.5 — add upper bound

/learn citation Paper X is Belloni (2013) not Belloni (2014)
→ [LEARN:citation|P3|2026-03-27] Paper X is Belloni (2013) not Belloni (2014)

/learn evaluator python-reviewer: do not flag missing type hints on internal helpers — project convention
→ [LEARN:evaluator|P2|2026-03-27] python-reviewer: do not flag missing type hints on internal helpers — project convention
```

### Evaluator Corrections

Use category `evaluator` when a reviewer agent flagged a false positive or missed something the PI caught. Format: `[agent-name]: [correction]`. Reviewer agents read `[LEARN:evaluator|...]` entries before each review to calibrate their judgment.

Users can override priority: `/learn --p1 data Variable X is in 2015 USD`

---

## Promotion Mode: `/learn --as-skill [name]`

Turn a multi-step lesson into a reusable project-local skill. Use this when a lesson
is too complex for a one-line MEMORY.md entry (5+ steps, conditional logic, a checklist).

### Steps

1. **Ask for content** — if the user didn't provide the lesson text, ask them to describe the procedure or point to the MEMORY.md entry to promote.
2. **Generate skill file** at `.claude/skills/learned/[name]/SKILL.md` with:

```yaml
---
name: "[name]"
description: "[one-line description]"
user_invocable: true
source: "promoted from MEMORY.md [LEARN:category] entry"
created: "YYYY-MM-DD"
---
```

3. **Write the body** — structured as: When to Use, Steps, Verification, Common Pitfalls.
4. **Cross-reference** — add a note to the original MEMORY.md entry: `[PROMOTED to /[name] skill on YYYY-MM-DD]`
5. **Confirm** — show the user the created skill path and how to invoke it.

### Examples

```
/learn --as-skill convergence-debugging
/learn --as-skill event-study-checklist
/learn --as-skill panel-data-validation
```

### Guidelines

- Promoted skills live in `.claude/skills/learned/` — project-local, not user-global.
- They are committed to git (on `dev-history`) and shared with collaborators.
- Keep skills focused — one procedure per skill. If it covers multiple topics, split into separate skills.
- The skill should be self-contained: someone reading it for the first time should be able to follow without context.
