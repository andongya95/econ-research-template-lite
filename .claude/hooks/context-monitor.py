#!/usr/bin/env python
"""
PostToolUse hook: monitors context usage via tool-call count and warns
progressively. Uses weighted token estimates per tool type; warnings fire
at estimated 40/55/65/80/90% of a 200k-token window.
Cross-platform (Windows/macOS/Linux).
"""
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import _utils


# Weighted token estimates by tool type
TOKENS_BY_TOOL = {
    "Read": 6000,
    "WebFetch": 8000,
    "WebSearch": 5000,
    "Bash": 4000,
    "Grep": 3000,
    "Write": 3000,
    "Edit": 2500,
    "Glob": 1500,
    "Task": 5000,
}
DEFAULT_TOKENS = 4000
CONTEXT_WINDOW = 680_000

THRESHOLDS = [
    (0.90, "CRITICAL — Context ~90%. STOP all polling loops and cancel any active Monitors. Save state NOW (MEMORY.md, plan, session log). Auto-compaction will fire shortly — do not start new tool calls that produce large output."),
    (0.80, "Context ~80%. STOP any repeated status-checking or polling. Save key decisions to session log, ensure plan is on disk. Finish current task step, then let auto-compaction reclaim space."),
    (0.65, "Context ~65%. Append recent decisions to session log. If polling a long-running process, switch to waiting for background completion notification instead."),
    (0.55, "Context ~55%. Consider updating session log with progress so far."),
    (0.40, "Context ~40%. Session is getting long — keep session log current."),
]

# How often to show each level (avoid spamming)
REMIND_EVERY = {0.90: 2, 0.80: 4, 0.65: 6, 0.55: 10, 0.40: 15}


def main():
    session_dir = _utils.get_session_dir()
    cache_path = session_dir / "context-monitor-cache.json"

    # Read hook input to get tool_name
    try:
        hook_input = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        hook_input = {}

    tool_name = hook_input.get("tool_name", "")
    tool_tokens = TOKENS_BY_TOOL.get(tool_name, DEFAULT_TOKENS)

    # Load or init
    cache = {"call_count": 0, "estimated_tokens": 0, "last_warned_at": {}}
    try:
        with open(cache_path, encoding="utf-8") as f:
            cache = json.load(f)
    except (OSError, json.JSONDecodeError):
        pass

    cache["call_count"] = cache.get("call_count", 0) + 1
    cache["estimated_tokens"] = cache.get("estimated_tokens", 0) + tool_tokens
    call_count = cache["call_count"]
    estimated_tokens = cache["estimated_tokens"]

    estimated_pct = estimated_tokens / CONTEXT_WINDOW

    # In autonomous mode, only block at 95%+ (CRITICAL save-state threshold)
    autonomous = _utils.is_autonomous_mode()

    # Check thresholds from highest to lowest
    for threshold, message in THRESHOLDS:
        if estimated_pct >= threshold:
            # In autonomous mode, skip all thresholds below 0.90
            if autonomous and threshold < 0.90:
                break

            last_warned = cache.get("last_warned_at", {}).get(str(threshold), 0)
            remind_every = REMIND_EVERY.get(threshold, 5)
            if (call_count - last_warned) >= remind_every:
                cache.setdefault("last_warned_at", {})[str(threshold)] = call_count
                # Never block — all thresholds are advisory.
                # Omit "decision" field entirely so compaction is not affected.
                output = {
                    "reason": f"[Context Monitor] ~{int(estimated_pct*100)}% used ({call_count} calls, ~{estimated_tokens:,} tokens). {message}",
                }
                json.dump(output, sys.stdout)
            break  # Only warn for highest applicable threshold

    # Single cache write — captures both counter update and last_warned_at
    try:
        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump(cache, f)
    except OSError:
        pass

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
