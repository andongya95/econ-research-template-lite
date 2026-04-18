---
paths: ["scripts/**", "stata/**", "R/**", "julia/**", "src/**", "explorations/**"]
---

# Dataset Isolation Protocol

Prevents cross-domain data contamination by locking the active dataset after
DATA_COLLECTION begins. Part of the human-oversight research principles.

---

## The Rule

Once the DATA_COLLECTION stage completes (all 5 pre-execution conditions RESOLVED and
`PIPELINE_STATE.md` shows `Active Dataset Lock` populated), the locked dataset(s) define
the analysis universe for this paper.

**Cross-domain joins are blocked by default.** A cross-domain join is any merge, join,
or append that introduces a dataset not listed in the Active Dataset Lock.

---

## What Triggers a Violation Flag

When writing or editing analysis code, check whether:

1. A file path appearing in a `pd.merge()`, `merge`, `use ... using`, `left_join()`, `cbind()`,
   or equivalent is **not** listed in `PIPELINE_STATE.md → Active Dataset Lock`
2. A loop or wildcard imports data from multiple domains (e.g., different surveys, admin
   records from different agencies)
3. A script imports data from both `data/raw/` and an external URL or API not audited

If any condition is met: **flag with a NOTICE** before writing the code.

---

## Unlock Procedure

If a cross-domain join is scientifically justified (e.g., merging a labor survey with
administrative earnings records when both are in scope):

1. Confirm with the PI
2. PI adds a `DATASET_UNLOCK` entry to `PIPELINE_STATE.md` (see `pipeline-state-protocol.md`)
   with: datasets joined, justification, date, PI name
3. Proceed with the join only after the unlock entry is committed

---

## Scope Clarification

**This protocol applies to:** cross-domain data mixing (different survey instruments,
different administrative sources, different time periods outside the defined sample).

**This does NOT block:** merging tables within the same dataset (e.g., merging firm-level
and worker-level files from the same admin database), or appending panel waves of the
same source.

---

## Why This Matters

Cross-domain mixing without explicit authorization is a common source of:
- Undisclosed sample selection (different coverage between datasets)
- Unit-of-observation mismatch (firm-level vs. worker-level, county vs. state)
- Vintage inconsistency (different reference years for "the same" variable)

Requiring an explicit unlock log creates an auditable record of every data integration
decision — consistent with the principle that authorship accountability demands
traceable human judgment at every non-trivial design choice.
