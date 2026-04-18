#!/usr/bin/env python
"""
Standalone script: computes review depth tier from git diff.
Called by orchestrator before dispatching reviewer agents.

Usage: python .claude/hooks/review-tier.py
Output: JSON with tier (LIGHT/STANDARD/FULL) and details.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import _utils


def main():
    tier, details = _utils.compute_review_tier()
    print(json.dumps({"tier": tier, **details}, indent=2))


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(json.dumps({"tier": "FULL", "lines_changed": -1, "files_changed": -1,
                          "new_files": False, "all_docs": False, "reason": f"error: {e}"}))
