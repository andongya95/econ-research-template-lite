---
name: econ-paper-writing
description: "Draft empirical econ papers for top journals. Identification, estimates, tables, LaTeX conventions."
last_updated: 2026-02-03
allowed-tools: Read
---

# Economics Paper Writing for Top Journals

Expert-level guidance for writing publication-ready empirical economics papers. This skill adapts the writing-review-revise philosophy from ML paper writing (proactive drafts, iterative feedback, citation verification) to economics: identification strategy, causal inference, data, and journal conventions.

**For polishing prose, wide tables, and journal-ready LaTeX formatting**, use the tex-journal-draft skill. This skill focuses on structure, workflow, and first-draft generation.

**Related skills:** econ-orchestrator (multi-stage coordination), research-repo-scanner (scan repo before drafting), python-econ-data / stata-reduced-form / structural-estimation (understand outputs from code).

---

## Core Philosophy: Collaborative Writing

**Paper writing is collaborative, but the agent should be proactive in delivering drafts.**

1. **Understand the project** by exploring the repo, data, code, and results
2. **Deliver a complete first draft** when confident about the contribution
3. **Search literature** using web search and APIs to find relevant citations
4. **Refine through feedback cycles** when the author provides input
5. **Ask for clarification** only when genuinely uncertain about key decisions

**Key Principle**: Be proactive. If the repo and results are clear, deliver a full draft. Don't block waiting for feedback on every section. Produce something concrete to react to, then iterate.

---

## ⚠️ CRITICAL: Never Hallucinate Citations

**NEVER generate BibTeX entries from memory. ALWAYS fetch programmatically.**

| Action | ✅ Correct | ❌ Wrong |
|--------|-----------|----------|
| Adding a citation | Search API → verify → fetch BibTeX | Write BibTeX from memory |
| Uncertain about a paper | Mark as `[CITATION NEEDED]` | Guess the reference |
| Can't find exact paper | Note: "placeholder - verify" | Invent similar-sounding paper |

If you cannot verify a citation:
```latex
% EXPLICIT PLACEHOLDER - requires human verification
\cite{PLACEHOLDER_author2024_verify_this}  % TODO: Verify this citation exists
```
**Always tell the author**: "I've marked [X] citations as placeholders that need verification."

For citation APIs: Semantic Scholar, CrossRef (DOI→BibTeX), arXiv. See [references/citation-workflow.md](references/citation-workflow.md) or 20-ml-paper-writing/references/citation-workflow.md.

---

## Workflow 0: Starting from a Research Repository

```
Project Understanding:
- [ ] Step 1: Explore the repository structure
- [ ] Step 2: Read README, docs, key results (tables, figures)
- [ ] Step 3: Identify the main contribution with the author
- [ ] Step 4: Find papers already cited in code or notes
- [ ] Step 5: Search for additional relevant literature
- [ ] Step 6: Outline the paper structure
- [ ] Step 7: Draft sections iteratively with feedback
```

**Step 1: Explore the Repository**
```bash
ls -la
find . -name "*.do" -o -name "*.m" -o -name "*.py" | head -30
find . -name "*.bib" -o -name "*.tex"
find . -path "*/results/*" -o -path "*/output/*" -o -path "*/tables/*"
```

Look for: `README`, `data/`, `code/`, `results/`, `tables/`, `.bib`, `.tex` drafts, Stata/MATLAB/Python scripts.

**Step 2: Identify Existing Citations**
```bash
grep -r "doi\|cite\|@article" --include="*.bib" --include="*.tex" --include="*.do" .
```

**Step 3: Clarify the Contribution**
> "Based on my understanding of the repo, the main contribution appears to be [X]. The key results show [Y]. Is this the framing you want, or should we emphasize different aspects?"

**Step 4–5**: Search literature; verify citations; deliver first draft. **Draft first, ask with the draft** (not before).

---

## Balancing Proactivity and Collaboration

| Confidence Level | Action |
|-----------------|--------|
| **High** (clear repo, obvious contribution) | Write full draft, deliver, iterate on feedback |
| **Medium** (some ambiguity) | Write draft with flagged uncertainties, continue |
| **Low** (major unknowns) | Ask 1-2 targeted questions, then draft |

**Draft first, ask with the draft:**

| Section | Draft Autonomously | Flag With Draft |
|---------|-------------------|-----------------|
| Abstract | Yes | "Framed contribution as X—adjust if needed" |
| Introduction | Yes | "Emphasized identification Y—correct if wrong" |
| Data | Yes | "Included variables A, B, C—add missing" |
| Empirical strategy | Yes | "Specification follows Z—confirm" |
| Results | Yes | "Highlighted tables 1–3—reorder if needed" |
| Mechanisms / robustness | Yes | "Cited papers X, Y—add any I missed" |

**Only block when:** Target journal unclear; contradictory framings; results incomplete; explicit request to review before continuing.

---

## The Narrative Principle (Economics Adaptation)

**Your paper is not a collection of regressions—it's a story with one clear contribution supported by evidence.**

| Pillar | Economics Interpretation | Example |
|--------|--------------------------|---------|
| **The What** | 1–3 specific empirical claims | "We show that X increases Y by Z percent" |
| **The Why** | Identification strategy and evidence | Variation exploited, assumptions, robustness |
| **The So What** | Policy relevance, mechanism, welfare | Why readers and policymakers should care |

**If you cannot state your contribution in one sentence, you don't yet have a paper.**

---

## Paper Structure Workflow

### Workflow 1: Writing a Complete Paper (Iterative)

**Each step: draft → feedback → revision.**

```
Paper Writing Progress:
- [ ] Step 1: Define the one-sentence contribution (with author)
- [ ] Step 2: Draft main figure (event-study or key result) → feedback → revise
- [ ] Step 3: Draft abstract → feedback → revise
- [ ] Step 4: Draft introduction (no "Introduction" heading in AER) → feedback → revise
- [ ] Step 5: Draft institutional background → feedback → revise
- [ ] Step 6: Draft data section → feedback → revise
- [ ] Step 7: Draft empirical strategy → feedback → revise
- [ ] Step 8: Draft results → feedback → revise
- [ ] Step 9: Draft mechanisms / heterogeneity → feedback → revise
- [ ] Step 10: Draft robustness → feedback → revise
- [ ] Step 11: Draft conclusion → feedback → revise
- [ ] Step 12: Simulate reviewer; final review cycle
```

**Step 1: Define the One-Sentence Contribution** (requires author confirmation)
> "I propose framing the contribution as: '[one sentence]'. Does this capture the main takeaway?"

**Step 3: Abstract (Economics: ~100–150 words)**
1. Core question (1 sentence)
2. Main findings (2–3 sentences)
3. Mechanism (1 sentence)
4. Bottom line (1 sentence)

Remove from abstracts: methodological details, secondary findings, robustness. Delete weak openings like "This paper studies..."

**Step 4: Introduction**
- Contribution, setting, preview
- Identification framing (what variation, what assumption)
- Claims must map to identification assumptions
- See [references/identification-language.md](references/identification-language.md)

**Economics paper structure:** See [references/structure-map.md](references/structure-map.md).

---

## AER Template Workflow

### Workflow 2: Starting a New Paper from AER Template

**Template location:** `templates/aer/` (copied from `Journal_Template_for_The_American_Economic_Review__AER_/`)

```
- [ ] Step 1: Copy entire AER template directory to new project
- [ ] Step 2: Verify template compiles as-is (pdflatex + bibtex × 2)
- [ ] Step 3: Replace title, authors, abstract, sections
- [ ] Step 4: Add your .bib file; update \bibliography{}
- [ ] Step 5: Add figures/tables; use figurenotes/tablenotes
```

**AER-specific:**
- No "Introduction" heading; begin introductory material before first `\section{}`
- Captions below figures, above tables
- Use `\begin{figurenotes}` and `\begin{tablenotes}` for notes
- Appendix after bibliography; use `\appendix`
- Use `aea` bibliography style with `aea.bst`

**Compilation:**
```bash
pdflatex AER-Article.tex
bibtex AER-Article
pdflatex AER-Article.tex
pdflatex AER-Article.tex
```

---

## Workflow 3: Creating Lecture / Seminar Slides from a Paper

**Goal:** Turn a working paper or published paper into a 45-min seminar talk (15–20 frames) or a course lecture.

### Frame Budget

| Section | Seminar (45 min) | Full lecture (90 min) |
|---------|------------------|-----------------------|
| Title + motivation | 2 | 2 |
| Setting / institutional background | 2–3 | 3–4 |
| Data | 2 | 3 |
| Identification strategy | 3–4 | 4–5 |
| Main results | 3–4 | 4–5 |
| Mechanisms / heterogeneity | 2 | 3–4 |
| Conclusion + takeaways | 1–2 | 2 |
| **Backup slides** | unlimited | unlimited |
| **Total (non-backup)** | **15–20** | **21–28** |

### Key Principles

1. **Results-forward.** Show the main result by frame 7–8. Don't make the audience wait.
2. **One idea per frame.** If you need more space, split into two frames.
3. **No overlay animations.** See `no-pause-beamer` rule. Every frame shows complete content.
4. **TikZ for intuition.** A timeline diagram of your DiD beats a wall of assumptions.
5. **Backup slides are free.** Robustness checks, data details, proofs → backup after `\appendix`.
6. **Figures adapted for slides** → larger fonts, bolder lines, simpler legends than paper figures.

### Beamer Template

```latex
\documentclass[aspectratio=169]{beamer}
\usetheme{default}
\usecolortheme{beaver}  % or Pittsburgh, Madrid, etc.
\setbeamertemplate{navigation symbols}{}  % remove nav bar

\title{Your Title}
\subtitle{Optional subtitle}
\author{Author Name}
\institute{University / Conference}
\date{\today}

\begin{document}

\frame{\titlepage}

\begin{frame}{Motivation}
  \begin{itemize}
    \item Key fact / puzzle that motivates the paper
    \item Why it matters for policy or theory
    \item What we do (one sentence)
  \end{itemize}
\end{frame}

\begin{frame}{Related Literature}
  \begin{itemize}
    \item \textbf{Strand 1:} Author (year) — what they do; \textbf{we add} X
    \item \textbf{Strand 2:} Author (year) — what they do; \textbf{we add} Y
    \item \textbf{Strand 3:} Author (year) — what they do; \textbf{we add} Z
  \end{itemize}
\end{frame}

% ... identification, results, mechanisms frames ...

\begin{frame}{Conclusion}
  \begin{itemize}
    \item \textbf{Main finding:} [one sentence]
    \item \textbf{Mechanism:} [one sentence]
    \item \textbf{Policy implication:} [one sentence]
  \end{itemize}
\end{frame}

\appendix

\begin{frame}{Backup: Robustness Checks}
  % Tables / figures showing robustness
\end{frame}

\end{document}
```

### Slides from Paper Checklist

```
- [ ] Reduce paper abstract to 3 bullets on motivation frame
- [ ] Pick ONE main result figure or table (not all tables)
- [ ] Create TikZ diagram for identification intuition
- [ ] Add "Contribution to Literature" frame (3-5 papers)
- [ ] Add "Data" frame with summary statistics or map
- [ ] Backup: data construction details
- [ ] Backup: robustness checks and alternative specs
- [ ] Test compilation: latexmk -pdf slides.tex
- [ ] Run /slide-excellence for quality audit before presenting
```

---

## Workflow 4: Deploying Slides

### Option A: PDF (standard distribution)

```bash
latexmk -pdf slides.tex
# → slides.pdf ready for email / conference upload
```

**Handout mode** (2 slides per A4 page for printing):
```latex
% In preamble:
\usepackage{pgfpages}
\pgfpagesuselayout{2 on 1}[a4paper,border shrink=5mm]
```
Or compile with: `pdflatex -jobname=slides_handout "\PassOptionsToClass{handout}{beamer}\input{slides.tex}"`

### Option B: GitHub Pages (shareable URL)

```bash
mkdir -p docs/slides
cp slides.pdf docs/slides/index.pdf
git add docs/slides && git commit -m "deploy slides"
git push
```
In GitHub: Settings → Pages → Source: main / `docs/`

**GitHub Actions auto-build** (`.github/workflows/deploy-slides.yml`):
```yaml
name: Deploy slides
on:
  push:
    paths: ['slides/**']
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: xu-cheng/latex-action@v3
        with:
          root_file: slides/slides.tex
      - run: mkdir -p docs/slides && cp slides.pdf docs/slides/
      - uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./docs
```

### Option C: Quarto HTML slides (interactive, shareable link)

```bash
# slides.qmd with format: revealjs
quarto render slides.qmd --to revealjs
quarto publish gh-pages slides.qmd
```

### Option D: Conference / journal supplementary material

Upload `slides.pdf` and `slides_handout.pdf` to the paper's OSF / GitHub release / journal supplementary files.

---

## Writing Philosophy (Universal)

These principles apply across fields; they improve clarity and reader comprehension.

**Gopen & Swan (7 principles):** Subject-verb proximity; stress position (emphasis at sentence end); topic position; old before new; one unit one function; action in verb; context before new.

**Ethan Perez:** Minimize pronouns ("This result shows" not "This shows"); verbs early; delete filler ("actually," "very," "really," "essentially").

**Lipton:** Be specific; eliminate hedging; avoid incremental vocabulary; delete intensifiers.

**Steinhardt:** Consistent terminology; state assumptions explicitly.

**What reviewers read:** Abstract (100%), Introduction (90%+), Figures (before body). Front-load contribution.

---

## Reviewer Evaluation (Economics Journals)

| Criterion | What Reviewers Look For |
|-----------|-------------------------|
| **Identification** | Clear variation, credible assumptions, robustness checks |
| **Clarity** | Reproducible, consistent notation, claims map to evidence |
| **Significance** | Policy relevance, mechanism, contribution to literature |
| **Originality** | New question, new data, new method, or new finding |

**Pre-submission self-check:** Would I trust these results? Can someone reproduce from the paper? Why should the field care? What specifically is new?

See [references/reviewer-guidelines-econ.md](references/reviewer-guidelines-econ.md) for journal-specific guidance and how to address referee reports.

---

## Tables and Figures

**Tables:** Use `booktabs` (`\toprule`, `\midrule`, `\bottomrule`). Bold best/most relevant estimates. Right-align numbers. For wide Stata tables: use `sidewaystable`, `\footnotesize`, shorten column names—see tex-journal-draft `references/wide-tables.md`.

**Figures:** Vector graphics (PDF/EPS). Colorblind-safe palettes. Self-contained captions. Event-study plots: show pre-trends, confidence intervals.

---

## References & Cross-Skills

| Document | Contents |
|----------|----------|
| [identification-language.md](references/identification-language.md) | Use "We exploit variation in..."; avoid "proves" |
| [structure-map.md](references/structure-map.md) | Canonical economics paper structure |
| [reviewer-guidelines-econ.md](references/reviewer-guidelines-econ.md) | Reviewer criteria, addressing reports |
| [citation-workflow.md](references/citation-workflow.md) | Verification APIs, BibTeX workflow |

**tex-journal-draft** (use for): Polish, de-AI-ify, wide tables, avoid bullets/inline stats/em dashes, fix citations, journal-ready prose.
