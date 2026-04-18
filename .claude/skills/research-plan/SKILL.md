---
name: research-plan
description: "Draft a Stage B research plan: question, identification, specification, robustness, power."
last_updated: 2026-02-26
allowed-tools: Read, Write, Glob, Grep, WebSearch
---

# Research Plan Skill

Draft a complete Stage B research plan before any analysis code is written. Follows `research-planning-protocol.md`.

## When to use

- After idea selection (post `/idea-ranking`) and Stage A `initial_plan.md` is approved
- When starting any new empirical analysis
- Before writing any `code/` scripts

## Required input

- **Research idea or topic:** What question are we answering?
- **Identification strategy:** What is the source of variation?
- **Dataset:** What data will be used?
- Optional: `initial_plan.md` path or `ideas.md` path from `/idea-ranking`

## Workflow

### 1. Read context
- Read `CLAUDE.md` for project context
- If `initial_plan.md` or `ideas.md` exist, read them
- If data documentation exists, read it (codebook, README, data dict)

### 2. Draft all required sections

Produce a complete `research_plan.md` with ALL of these sections:

**§1. Research Question**
1–2 sentences. Should be answerable by the data.

**§2. Identification Strategy**
- Source of variation (what is the treatment? who? when?)
- Treatment definition with exact cohort timing
- Control group definition
- Key identifying assumption (state formally, e.g., "parallel trends: absent treatment, treated and control states would have followed parallel trends in Y")

**§3. Primary Specification**
- Display equation with all terms defined (use LaTeX notation if appropriate)
- Fixed effects (level and justification)
- Clustering (level and justification)
- Estimator (name and cite if non-standard)

**§4. Expected Effects and Mechanisms**
- Theoretical prediction: sign, rough magnitude, and why
- Mechanism: economic channel through which treatment affects outcome
- Key heterogeneity dimensions (at least 2)

**§5. Planned Robustness Checks (≥8)**
Label R1–R8+. Must include:
- R_: Event study / pre-trend test (always required)
- R_: Placebo test (wrong group, wrong time, or wrong outcome)
- R_: Alternative estimator or specification
- R_: Permutation or randomization inference
- R_: Sample restriction robustness

**§6. Data Sources**
For each dataset:
- Name, URL or local path
- Authentication needed (API key, credentials)
- Time period, geographic coverage, unit of observation
- Any known data limitations

**§7. Power Assessment**
- Pre-treatment periods
- Treated clusters/units
- Control clusters/units
- Minimum detectable effect (MDE) estimate
- Known constraints (short pre-period, few clusters, etc.)

**§8. Known Limitations and Planned Responses**
3 anticipated referee concerns + how to address each.

### 3. Save output

Save to: `quality_reports/plans/YYYY-MM-DD_[paper-name]-research-plan.md`

Add frontmatter:
```markdown
---
status: DRAFT
paper: [paper name]
date: YYYY-MM-DD
method: [DiD/IV/RDD/etc.]
data: [dataset name]
---
```

### 4. Present for approval

Present the plan to the user. Ask for approval before any coding begins.
After approval, update frontmatter status to `APPROVED`.

### 5. Transition

After approval: "Next step: resolve pre-execution conditions using the conditions protocol before writing any analysis code."

## Output to user

1. Complete `research_plan.md` content displayed
2. File saved path
3. Request explicit approval before coding
