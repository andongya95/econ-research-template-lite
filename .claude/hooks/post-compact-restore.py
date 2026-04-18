#!/usr/bin/env python
"""
Post-compact restore hook: fires after session compaction to restore context.
Points Claude at the saved plan and recent decisions.
Archives pre-compact state instead of deleting. Resets first-prompt-done flag
so session-start-context.py re-fires after compaction.
Cross-platform (Windows/macOS/Linux).
"""
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import _utils


def main():
    # Only meaningful after compaction/resume events
    event = os.environ.get("CLAUDE_SESSION_TYPE", "")
    if event not in ("compact", "resume", ""):
        sys.exit(0)

    session_dir = _utils.get_session_dir()

    # Reset context-monitor counter so a fresh session starts from 0
    try:
        (session_dir / "context-monitor-cache.json").unlink(missing_ok=True)
    except OSError:
        pass

    # Reset first-prompt-done flag so session-start-context.py re-fires
    try:
        (session_dir / "first-prompt-done").unlink(missing_ok=True)
    except OSError:
        pass

    state_file = session_dir / "pre-compact-state.json"

    state = None
    if state_file.exists():
        try:
            with open(state_file, encoding="utf-8") as f:
                state = json.load(f)
            # Archive instead of deleting
            archive_dir = session_dir / "archive"
            archive_dir.mkdir(exist_ok=True)
            ts = state.get("timestamp", "unknown").replace(":", "-")
            state_file.rename(archive_dir / f"pre-compact-state-{ts}.json")
            # Prune: keep only last 3 archives
            archives = sorted(
                archive_dir.glob("pre-compact-state-*.json"),
                key=lambda p: p.stat().st_mtime,
                reverse=True,
            )
            for old in archives[3:]:
                old.unlink(missing_ok=True)
        except (OSError, json.JSONDecodeError):
            pass

    plan_file, _ = _utils.find_active_plan()
    log_file = _utils.find_latest_session_log()

    lines = ["[Post-compact restore] Context recovery summary:\n"]

    if state:
        if state.get("plan_file"):
            lines.append(f"  Active plan:  {state['plan_file']}")
        if state.get("current_task"):
            lines.append(f"  Current task: {state['current_task']}")
        if state.get("recent_decisions"):
            lines.append("  Recent decisions:")
            for d in state["recent_decisions"][:3]:
                lines.append(f"    \u2022 {d}")
    else:
        if plan_file:
            lines.append(f"  Latest plan:  {plan_file}")

    if log_file:
        lines.append(f"  Session log:  {log_file}")

    lines.append("")
    if plan_file:
        lines.append(f"\u2192 To resume: read {plan_file} and git log --oneline -5")
    lines.append("\u2192 Also read CLAUDE.md and check MEMORY.md for [LEARN] entries")

    # In autonomous mode: provide context info but don't block — continue working
    decision = "allow" if _utils.is_autonomous_mode() else "block"
    output = {
        "decision": decision,
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
