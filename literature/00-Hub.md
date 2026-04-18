# Literature Vault

Central entry point for the project's literature knowledge base.

## Sections

- [[#Papers]] — One reading note per paper (`papers/`)
- [[#Topics]] — Thematic overviews linking related papers (`topics/`)
- [[#Methods]] — Estimator and technique notes (`methods/`)
- [[#Datasets]] — Data source documentation (`datasets/`)

## Quick Links

- `references.bib` — Canonical BibTeX file (paper/*.tex cites from here)
- `papers/_template.md` — Template for new reading notes
- `datasets/_template.md` — Template for new dataset notes

---

## Papers

```dataview
TABLE status, relevance, journal, year
FROM "papers"
WHERE citekey
SORT relevance DESC
```

### By Status

```dataview
TABLE length(rows) AS "Count"
FROM "papers"
WHERE citekey
GROUP BY status
```

---

## Topics

```dataview
LIST
FROM "topics"
SORT file.name ASC
```

---

## Methods

```dataview
LIST
FROM "methods"
SORT file.name ASC
```

---

## Datasets

```dataview
TABLE source, years, unit, status
FROM "datasets"
WHERE name
SORT file.name ASC
```

---

## Recently Added

```dataview
TABLE title, status, relevance
FROM "papers"
WHERE citekey
SORT file.ctime DESC
LIMIT 10
```
