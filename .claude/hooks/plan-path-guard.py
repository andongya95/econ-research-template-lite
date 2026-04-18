#!/usr/bin/env python
"""
PreToolUse hook (Write): blocks plan-like content from being saved to sessions/.
Plans belong in quality_reports/plans/, not quality_reports/sessions/.
Cross-platform (Windows/macOS/Linux).
"""
import json
import re
import sys


# Markers that indicate plan-like content (not session logs)
PLAN_MARKERS = [
    "## Approach",
    "## Steps",
    "## Files to modify",
    "## Files to Modify",
    "Status: DRAFT",
    "Status: APPROVED",
    "Status: IN_PROGRESS",
    "Status: IN-PROGRESS",
    "**Status:** DRAFT",
    "**Status:** APPROVED",
    "**Status:** IN_PROGRESS",
    "**Status:** IN-PROGRESS",
    "## Implementation Steps",
    "## Verification Plan",
    "## Phase 1",
]

# Minimum number of markers required to trigger block (3 reduces false positives)
MIN_MARKERS = 3


def main():
    try:
        hook_input = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        sys.exit(0)

    file_path = hook_input.get("file_path", "")
    content = hook_input.get("content", "")

    if not file_path or not content:
        sys.exit(0)

    # Normalize path separators
    normalized_path = file_path.replace("\\", "/")

    # Early exit: only check sessions/ and plans/ paths
    is_session = "quality_reports/sessions/" in normalized_path
    is_plan = "quality_reports/plans/" in normalized_path
    if not is_session and not is_plan:
        sys.exit(0)

    # Guard 1: block plans saved to sessions/
    if is_session:
        marker_count = sum(1 for marker in PLAN_MARKERS if marker in content)
        if marker_count >= MIN_MARKERS:
            output = {
                "decision": "block",
                "reason": (
                    f"This looks like a PLAN being saved to sessions/. "
                    f"Plans belong in quality_reports/plans/, not quality_reports/sessions/. "
                    f"Detected {marker_count} plan markers: change the path to "
                    f"quality_reports/plans/YYYY-MM-DD_description.md"
                ),
            }
            json.dump(output, sys.stdout)
            sys.exit(0)

    # Guard 2: warn if plan is marked APPROVED/IN_PROGRESS but has no success criteria
    if is_plan:
        is_approving = bool(re.search(
            r'\*{0,2}status\*{0,2}\s*[:\s]\s*\*{0,2}\s*(approved|in.progress)',
            content, re.IGNORECASE
        ))
        if is_approving:
            # Find ### Success Criteria header and check for at least one checkbox after it
            criteria_match = re.search(r'### Success Criteria', content)
            if not criteria_match:
                output = {
                    "decision": "block",
                    "reason": (
                        "Plan is being marked APPROVED but has no Success Criteria. "
                        "Add '### Success Criteria' with testable '- [ ]' items to each step "
                        "before approving. See plan-first-workflow.md for the format."
                    ),
                }
                json.dump(output, sys.stdout)
                sys.exit(0)
            else:
                # Header exists — check that at least 1 '- [ ]' line follows
                after_header = content[criteria_match.end():]
                if not re.search(r'- \[ \]', after_header):
                    output = {
                        "decision": "block",
                        "reason": (
                            "Plan has '### Success Criteria' header but no checkboxes. "
                            "Add at least one '- [ ]' item under Success Criteria "
                            "before approving. See plan-first-workflow.md for the format."
                        ),
                    }
                    json.dump(output, sys.stdout)
                    sys.exit(0)

    sys.exit(0)


if __name__ == "__main__":
    try:
        main()
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
