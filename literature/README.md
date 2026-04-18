# Literature Vault

This folder is an [Obsidian](https://obsidian.md/) vault for managing reading notes, citations, and literature knowledge.

## Quick Start

1. Open Obsidian and select "Open folder as vault"
2. Point it to this `literature/` folder
3. Install recommended plugins (see below)

## Structure

```
literature/
├── 00-Hub.md           # Vault entry point — start here (Dataview queries)
├── references.bib      # Canonical BibTeX file — paper/*.tex cites from here
├── papers/             # One reading note per paper (use _template.md)
│   └── _template.md    # Copy this for each new paper
├── datasets/           # One note per dataset (provenance, quirks, variables)
│   └── _template.md    # Copy this for each new dataset
├── topics/             # Thematic overview notes (link to paper notes)
└── methods/            # Methodology notes (estimators, techniques)
```

## Conventions

### Hub Page (`00-Hub.md`)

- Entry point for the vault — open this first in Obsidian
- Contains Dataview queries for paper stats, recent additions, and section listings
- Links to all subdirectories

### Reading Notes (`papers/`)

- **One file per paper**, named `{firstauthor}{year}_{keyword}.md`
  - Examples: `callaway2021_did.md`, `dechaisemartin2020_twfe.md`, `roth2023_pretrends.md`
- **YAML frontmatter is required** — Claude agents parse it for metadata
- Copy `papers/_template.md` when adding a new paper
- Key frontmatter fields:
  - `citekey` — matches the BibTeX key in `references.bib`
  - `relevance` — 1 (tangential) to 5 (direct competitor)
  - `status` — `unread` | `reading` | `read` | `cited`

### Topic Notes (`topics/`)

- Overview notes that link to multiple paper notes
- Example: `topics/staggered-did.md` links to all papers on staggered DiD
- Use `[[wikilinks]]` to connect to paper notes in Obsidian

### Method Notes (`methods/`)

- Notes on specific estimators or techniques
- Example: `methods/callaway-santanna.md` explains the CS-DiD estimator
- Link to paper notes that use or introduce the method

### Dataset Notes (`datasets/`)

- One note per dataset, named `{source_shortname}.md`
  - Examples: `acs_5year.md`, `qcew.md`, `psid.md`
- YAML frontmatter is required — includes `name`, `source`, `years`, `unit`, `status`
- Copy `datasets/_template.md` when adding a new dataset
- Status values: `raw` | `cleaned` | `integrated` | `deprecated`

### BibTeX (`references.bib`)

- Single canonical file for the project
- `paper/*.tex` should `\bibliography{../literature/references.bib}`
- Append new entries at the end; do not reorder
- Key format: `firstauthor_year_keyword`

### Relevance Scores

| Score | Meaning |
|-------|---------|
| 1 | Tangential — cited for background only |
| 2 | Related — same broad topic |
| 3 | Important — uses similar method or studies similar outcome |
| 4 | Key predecessor — directly builds on this paper |
| 5 | Direct competitor — studies the same question |

## Recommended Obsidian Plugins

| Plugin | Purpose |
|--------|---------|
| **Citations** | Reads `references.bib`; auto-creates notes from BibTeX entries |
| **Dataview** | Query reading notes by tag, relevance, status (e.g., `TABLE WHERE relevance >= 4`) |
| **Templates** | Use `papers/_template.md` for new reading notes |
| **Zotero Integration** | Optional — sync with Zotero if you already use it |

### Citations Plugin Setup

1. Install "Citations" from Community Plugins
2. Set citation database path to `references.bib` (relative to vault root)
3. Set literature note folder to `papers/`
4. Set literature note template to `papers/_template.md`

## Git

- `.obsidian/` is gitignored (personal Obsidian config: themes, hotkeys, workspace)
- All vault content (notes, BibTeX) is committed and shared
- PDFs can be stored here but are gitignored by default (`.pdf` in `.gitignore`)
