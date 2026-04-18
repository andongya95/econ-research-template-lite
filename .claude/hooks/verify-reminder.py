#!/usr/bin/env python
"""
Verify Reminder Hook: PostToolUse on Write|Edit

After Claude edits a code file, reminds it what verification to run
before marking the task done. Non-blocking info message.

Skips: markdown, text, config, JSON, YAML, gitignore, requirements.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import _utils


# Per-extension verification commands
VERIFY_MAP = {
    ".py":   "▶  Verify: python {name} (or pytest {name} if test file)",
    ".do":   "▶  Verify: stata -b do {name}  (check .log for errors)",
    ".m":    "▶  Verify: matlab -batch \"run('{name}')\"",
    ".R":    "▶  Verify: Rscript {name}",
    ".tex":  "▶  Verify: latexmk -pdf {name}  (check overfull/undefined refs)",
    ".qmd":  "▶  Verify: quarto render {name}",
    ".sh":   "▶  Verify: bash -n {name}  (syntax check)",
    ".ps1":  "▶  Verify: pwsh -NonInteractive -File {name}",
    ".jl":   "▶  Verify: julia {name}",
    ".ipynb": "▶  Verify: jupyter nbconvert --to notebook --execute {name}",
}

# Extensions to skip silently
SKIP_EXTENSIONS = {
    ".md", ".txt", ".rst", ".json", ".yaml", ".yml", ".toml",
    ".cfg", ".ini", ".env", ".gitignore", ".gitattributes",
    ".csv", ".tsv", ".bib", ".cls", ".sty", ".log",
}


def main() -> int:
    try:
        hook_input = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        return 0

    # Extract file path from tool input
    tool_input = hook_input.get("tool_input", {})
    file_path = tool_input.get("file_path", tool_input.get("path", ""))

    if not file_path:
        return 0

    ext = Path(file_path).suffix.lower()
    name = Path(file_path).name

    # Skip non-code files
    if ext in SKIP_EXTENSIONS or not ext:
        return 0

    # Look up verification reminder
    reminder = VERIFY_MAP.get(ext)
    if not reminder:
        return 0

    # In autonomous mode: info-only, don't block
    if _utils.is_autonomous_mode():
        return 0

    # Use "approve" with reason — shows the reminder without interrupting flow.
    # "block" on PostToolUse causes the orchestrator to stall after every edit.
    output = {"decision": "approve", "reason": reminder.format(name=name)}
    json.dump(output, sys.stdout)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        try:
            from pathlib import Path as _P
            from datetime import datetime as _dt
            _log = _P.home() / ".claude" / "hook-errors" / "errors.log"
            _log.parent.mkdir(parents=True, exist_ok=True)
            with _log.open("a") as _fh:
                _fh.write(f"{_dt.now().isoformat()} {_P(__file__).name}: {e}\n")
        except Exception:
            pass
        sys.exit(0)
