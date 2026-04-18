---
paths:
  - "quality_reports/paps/**"
  - "scripts/**"
  - "stata/**"
  - "src/**"
---

# Pre-Analysis Plan (PAP) Protocol

**Core principle:** Lock all empirical specifications BEFORE touching real data. A PAP is both a credibility commitment and a code-generation specification.

## When to Create a PAP
Create a PAP whenever:
- Starting a new empirical analysis
- Writing code that accesses real data
- Proposing a new specification or robustness check not already covered

Skip PAPs for:
- Explorations in `explorations/` (document in exploration notes instead)
- Pure replication of an existing paper (use `quality_reports/[project]_replication_targets.md` instead)
- Purely synthetic data exercises

## PAP Workflow
1. **CREATE** → Use `.claude/templates/pap-template.md`; save as `quality_reports/paps/YYYY-MM-DD_topic.md`; fill ALL sections.
2. **REVIEW** → Read through PAP with user before locking; verify variable names and API endpoint are exact and accessible.
3. **LOCK** → Generate checksum `sha256sum quality_reports/paps/YYYY-MM-DD_topic.md`; paste hash into Checksum field; commit: `git commit -m "Lock PAP: [topic]"`.
4. **CODE** → Provide the locked PAP to the analysis agent. Agent uses §8 Technical Specification and §3 Data Specification for exact names.
5. **AMEND** → If design changes after locking, create `quality_reports/paps/YYYY-MM-DD_topic_v2.md`; note "Amendment to v1" with reason; never overwrite a locked PAP.

## Technical Specification Section is Critical
Section §8 must include:
- Exact column names from the dataset (wrong names cause runtime failures)
- Exact API endpoint (public data only; no auth)
- Package names (e.g., `csdid`, `did`, `reghdfe`, `fixest`)
- Expected output filenames (paper will `\input{}` these)

Missing or vague technical specifications are the primary cause of analysis code failures.

## Data Integrity
If real data is unavailable (API down, variable discontinued, sample too small):
- Append a note to the PAP
- Pivot to a different research question rather than fabricating data
- Never present synthetic data as real

## Storage
- PAPs live in `quality_reports/paps/`
- Template at `.claude/templates/pap-template.md`
