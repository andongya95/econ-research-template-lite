# Citation Verification for Economics Papers

**Rule: Never generate BibTeX from memory. Always verify programmatically.**

## APIs

| API | Use |
|-----|-----|
| Semantic Scholar | Search economics papers |
| CrossRef | DOI → BibTeX (content negotiation) |
| arXiv | Preprints, NBER WPs often on arXiv |

## Workflow

1. **Search** via Semantic Scholar or web
2. **Verify** paper exists in 2+ sources
3. **Retrieve** BibTeX via DOI: `https://doi.org/{doi}` with `Accept: application/x-bibtex`
4. **Validate** the attributed claim appears in the paper
5. **If any step fails** → mark as placeholder, inform author

## Python Example (DOI to BibTeX)

```python
import requests

def doi_to_bibtex(doi: str) -> str:
    response = requests.get(
        f"https://doi.org/{doi}",
        headers={"Accept": "application/x-bibtex"}
    )
    response.raise_for_status()
    return response.text
```

## Placeholder Format

```latex
\cite{PLACEHOLDER_author2024_verify}  % TODO: Verify - scientist must confirm
```

For full workflow and API details, see 20-ml-paper-writing/references/citation-workflow.md.
