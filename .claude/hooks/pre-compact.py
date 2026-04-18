#!/usr/bin/env python
"""
Pre-compact hook: saves active plan, current task, and recent decisions
to disk before context compaction. Cross-platform (Windows/macOS/Linux).
"""
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import _utils


def _get_recent_commits(n=5) -> str:
    """Return last n git log lines as a string, or a fallback message."""
    try:
        r = subprocess.run(
            ["git", "log", "--oneline", f"-{n}"],
            capture_output=True, text=True, timeout=5
        )
        if r.returncode == 0 and r.stdout.strip():
            return r.stdout.strip()
    except (OSError, subprocess.TimeoutExpired):
        pass
    return "(git log unavailable)"


def main():
    session_dir = _utils.get_session_dir()
    plan_file, current_task = _utils.find_active_plan()
    recent_decisions = _utils.find_recent_decisions()
    today = datetime.now().strftime("%Y-%m-%d")

    state = {
        "timestamp": datetime.now().isoformat(),
        "plan_file": plan_file,
        "current_task": current_task,
        "recent_decisions": recent_decisions,
    }
    state_path = session_dir / "pre-compact-state.json"
    try:
        with open(state_path, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)
    except OSError:
        pass

    # Append compaction note to most recent session log, or auto-create one
    latest_log = _utils.find_latest_session_log()
    if latest_log is None:
        # Auto-create minimal session log before context is lost
        sessions_dir = Path("quality_reports/sessions")
        sessions_dir.mkdir(parents=True, exist_ok=True)
        auto_path = sessions_dir / f"{today}_auto-checkpoint.md"

        recent_commits = _get_recent_commits(5)
        decisions_text = "\n".join(f"- {d}" for d in recent_decisions) or "- (none recorded)"

        auto_content = (
            f"# Session Log: Auto-Checkpoint (pre-compact)\n"
            f"**Date:** {today}\n"
            f"**Goal:** (auto-created — no session log existed at compaction time)\n\n"
            f"## Active Plan\n{plan_file or '(none)'}\n"
            f"Current task: {current_task or '(none)'}\n\n"
            f"## Recent Commits\n{recent_commits}\n\n"
            f"## Recent Decisions\n{decisions_text}\n\n"
            f"## Progress Log\n"
            f"- [{datetime.now().strftime('%H:%M')}] [PRE-COMPACT] Auto-compaction triggered. "
            f"Session log auto-created.\n"
        )
        try:
            auto_path.write_text(auto_content, encoding="utf-8")
            latest_log = auto_path
        except OSError:
            pass
    else:
        # Append compaction marker to existing log
        try:
            with open(latest_log, "a", encoding="utf-8") as f:
                f.write(f"\n\n---\n**[PRE-COMPACT {today}]** Auto-compaction triggered.\n")
                if current_task:
                    f.write(f"Current task: {current_task}\n")
        except OSError:
            pass

    plan_status = "YES" if plan_file else "NO — save to quality_reports/plans/ before compacting!"

    # Read hook input to check trigger type (auto vs manual)
    try:
        hook_input = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        hook_input = {}
    trigger = hook_input.get("trigger", "unknown")

    # NEVER block compaction. Blocking when context is exhausted creates an
    # unrecoverable deadlock — the agent can't complete the checklist because
    # context is full, and can't compact because the hook blocks it.
    # State is already saved to disk above; the checklist is advisory only.
    if trigger == "auto" or _utils.is_autonomous_mode():
        # Auto-compaction / autonomous: save state silently, no checklist
        output = {
            "reason": (
                f"[Pre-compact] State saved to {state_path}. "
                f"Plan: {plan_file or 'none'}. "
                f"Task: {current_task or 'none'}. "
                f"Decisions: {len(recent_decisions)} saved."
            ),
        }
    else:
        # Manual /compact: show advisory checklist but allow compaction
        output = {
            "reason": (
                f"[Pre-compact] State saved to {state_path}\n"
                f"  Plan:         {plan_file or 'none'}\n"
                f"  Current task: {current_task or 'none'}\n"
                f"  Decisions:    {len(recent_decisions)} saved\n\n"
                f"Advisory checklist (act on these after compaction if not yet done):\n"
                f"  [ ] MEMORY.md updated with [LEARN] entries?\n"
                f"  [x] Session log: {latest_log or 'NONE'}\n"
                f"  [{'x' if plan_file else ' '}] Plan saved to disk? {plan_status}\n"
                f"  [ ] Open questions documented in session log?\n"
            ),
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
