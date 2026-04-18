#!/usr/bin/env python
"""
UserPromptSubmit hook: injects last-session context on the first prompt of a session.
Uses a 'first-prompt-done' flag file to fire only once per session.
Also fires after compaction (flag is reset by post-compact-restore.py).
Cross-platform (Windows/macOS/Linux).
"""
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import _utils


def _retrieve_memory_block(user_message: str) -> str:
    """Query-based memory retrieval — returns formatted block or empty string."""
    selected, total = _utils.retrieve_memory(user_message)
    if not selected:
        return ""
    p1_count = sum(1 for e in selected if e["priority"] == 1)
    matched_count = len(selected) - p1_count
    lines = [f"[Memory] Loaded {len(selected)}/{total} entries ({p1_count} P1, {matched_count} matched):"]
    for e in selected:
        lines.append(f"  [P{e['priority']}|{e['category']}] {e['text']}")
    return "\n".join(lines)


def main():
    session_dir = _utils.get_session_dir()
    flag_file = session_dir / "first-prompt-done"

    # If flag exists, this is not the first prompt — exit immediately
    if flag_file.exists():
        sys.exit(0)

    # Create flag file so we don't fire again
    try:
        flag_file.write_text("1", encoding="utf-8")
    except OSError:
        pass

    # Read user message from stdin for memory retrieval
    user_message = ""
    try:
        hook_input = json.load(sys.stdin)
        user_message = hook_input.get("message", "")
    except (json.JSONDecodeError, EOFError):
        pass

    # Read last-session-summary.json (written by stop-checkpoint.py)
    summary_path = session_dir / "last-session-summary.json"
    summary = None
    if summary_path.exists():
        try:
            with open(summary_path, encoding="utf-8") as f:
                summary = json.load(f)
        except (OSError, json.JSONDecodeError):
            pass

    if summary:
        lines = [
            "[Session Context] Continuing from previous session "
            f"({summary.get('timestamp', 'unknown time')}):"
        ]

        if summary.get("active_plan"):
            lines.append(f"  Last plan:  {summary['active_plan']}")
        if summary.get("latest_session_log"):
            lines.append(f"  Last log:   {summary['latest_session_log']}")
        if summary.get("git_head"):
            lines.append(f"  Git HEAD:   {summary['git_head']}")
        if summary.get("response_count"):
            lines.append(f"  Responses:  {summary['response_count']}")

        decisions = summary.get("recent_decisions", [])
        if decisions:
            lines.append("  Recent decisions:")
            for d in decisions[:3]:
                lines.append(f"    - {d}")

        lines.append("")
        if summary.get("active_plan"):
            lines.append(f"-> Read {summary['active_plan']} and session log to re-orient.")
    else:
        lines = [
            "[Session Context] No previous session state found.",
            "-> Read CLAUDE.md for project context.",
            "-> Run `git log --oneline -5` to see recent work.",
        ]

    # Short-term memory injection (recent events, last 5)
    _utils.prune_short_term_memory()
    recent_entries = _utils.load_short_term_memory(5)
    if recent_entries:
        lines.append("## Recent Context (short-term memory)")
        for e in recent_entries:
            lines.append(f"  {e}")
        lines.append("")

    # Query-based memory retrieval
    memory_block = _retrieve_memory_block(user_message)
    if memory_block:
        lines.append("")
        lines.append(memory_block)
    else:
        lines.append("-> Check MEMORY.md for [LEARN] entries.")

    output = {
        "decision": "allow",
        "reason": "\n".join(lines),
    }
    json.dump(output, sys.stdout)
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
