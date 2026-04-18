#!/usr/bin/env python
"""
Stop hook: rolling snapshot ("black box recorder") + periodic log nagging.
Replaces log-reminder.py with richer functionality:
  A) Rolling snapshot — writes last-session-summary.json on every response
  B) Periodic log nagging — re-nags every RENAG_INTERVAL responses (not one-shot)
  C) Session log chaining — inserts "Continues from:" pointer in new logs
  D) MEMORY.md nudge — gentle reminder every MEMORY_NUDGE_INTERVAL responses
Cross-platform (Windows/macOS/Linux).
"""
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import _utils

# --- Configuration ---
FIRST_NAG_THRESHOLD = 8    # responses before first log nag
RENAG_INTERVAL = 6         # re-nag every N additional responses
MAX_NAGS_PER_CYCLE = 5     # cap nags to avoid infinite blocking
MEMORY_NUDGE_INTERVAL = 20 # nudge about MEMORY.md every N responses


def load_state(state_path: Path) -> dict:
    if state_path.exists():
        try:
            with open(state_path, encoding="utf-8") as f:
                return json.load(f)
        except (OSError, json.JSONDecodeError):
            pass
    return {
        "response_count": 0,
        "nag_count": 0,
        "last_log_mtime": None,
        "last_log_path": None,
        "session_start_time": time.time(),
        "memory_mtime_at_start": None,
        "no_log_reminded": False,
    }


def save_state(state_path: Path, state: dict):
    try:
        with open(state_path, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)
    except OSError:
        pass


def write_rolling_snapshot(session_dir: Path, state: dict):
    """Write last-session-summary.json — the black box recorder."""
    plan_file, current_task = _utils.find_active_plan()
    decisions = _utils.find_recent_decisions(3)
    git_head = _utils.get_git_head()
    latest_log = _utils.find_latest_session_log()

    snapshot = {
        "timestamp": datetime.now().isoformat(),
        "session_start_time": state.get("session_start_time", time.time()),
        "active_plan": plan_file,
        "current_task": current_task,
        "latest_session_log": str(latest_log) if latest_log else None,
        "recent_decisions": decisions,
        "response_count": state.get("response_count", 0),
        "git_head": git_head,
    }

    snapshot_path = session_dir / "last-session-summary.json"
    try:
        with open(snapshot_path, "w", encoding="utf-8") as f:
            json.dump(snapshot, f, indent=2)
    except OSError:
        pass


def check_session_log_chaining(latest_log: "Path | None", session_dir: Path):
    """If a new session log appeared recently, ensure it has a 'Continues from:' pointer."""
    if not latest_log:
        return

    try:
        log_mtime = latest_log.stat().st_mtime
    except OSError:
        return

    # Only chain if log was created/modified very recently (< 60s)
    if time.time() - log_mtime > 60:
        return

    # Read current content
    try:
        content = latest_log.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return

    # Already has a "Continues from" pointer
    if "Continues from:" in content or "continues from:" in content.lower():
        return

    # Find the previous session log (from our state tracking)
    last_log_path_file = session_dir / "last-log-path.txt"
    if not last_log_path_file.exists():
        return

    try:
        prev_log = last_log_path_file.read_text(encoding="utf-8").strip()
    except OSError:
        return

    if not prev_log or prev_log == str(latest_log):
        return

    # Insert "Continues from:" after the first heading or date line
    lines = content.split("\n")
    insert_idx = 0
    for i, line in enumerate(lines):
        if line.startswith("**Date:") or line.startswith("**Goal:"):
            insert_idx = i + 1
            break
        if i > 5:
            insert_idx = 2  # fallback: after first 2 lines
            break

    if insert_idx == 0:
        insert_idx = min(2, len(lines))

    pointer_line = f"**Continues from:** {prev_log}"
    lines.insert(insert_idx, pointer_line)

    try:
        latest_log.write_text("\n".join(lines), encoding="utf-8")
    except OSError:
        pass


def _capture_short_term_events(session_dir: Path, state: dict,
                                latest_log: "Path | None"):
    """Write commit and plan-change events to short-term rolling memory."""
    session_label = latest_log.stem if latest_log else datetime.now().strftime("%Y-%m-%d")

    # 1. New commit since last stop (hash-file guard prevents duplicates)
    hash_file = session_dir / "commit-logger-last-hash.txt"
    last_hash = ""
    if hash_file.exists():
        try:
            last_hash = hash_file.read_text(encoding="utf-8").strip()
        except OSError:
            pass
    git_head = _utils.get_git_head()
    current_hash = git_head.split()[0] if git_head else ""
    if current_hash and current_hash != last_hash:
        _utils.update_short_term_memory("commit", git_head, session_label)
        try:
            hash_file.write_text(current_hash, encoding="utf-8")
        except OSError:
            pass

    # 2. Plan task change (tool_count omitted — already in rolling snapshot JSON)
    _, current_task = _utils.find_active_plan()
    last_task = state.get("last_known_task", "")
    if current_task and current_task != last_task:
        _utils.update_short_term_memory("plan_change", current_task[:80], session_label)
        state["last_known_task"] = current_task


def main():
    # Read hook input
    try:
        hook_input = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        hook_input = {}

    if hook_input.get("stop_hook_active", False):
        sys.exit(0)

    session_dir = _utils.get_session_dir()
    state_path = session_dir / "stop-checkpoint-state.json"
    state = load_state(state_path)

    today = datetime.now().strftime("%Y-%m-%d")
    latest_log = _utils.find_latest_session_log()

    # Increment response count
    state["response_count"] = state.get("response_count", 0) + 1
    count = state["response_count"]

    # Initialize session start time and memory mtime on first response
    if count == 1:
        state["session_start_time"] = time.time()
        mem_path = Path("MEMORY.md")
        if mem_path.exists():
            try:
                state["memory_mtime_at_start"] = mem_path.stat().st_mtime
            except OSError:
                pass

    # --- A) Rolling snapshot (always) ---
    write_rolling_snapshot(session_dir, state)

    # --- A2) Short-term event capture ---
    _capture_short_term_events(session_dir, state, latest_log)

    # --- C) Session log chaining ---
    check_session_log_chaining(latest_log, session_dir)

    # Track the latest log path for future chaining
    if latest_log:
        try:
            (session_dir / "last-log-path.txt").write_text(
                str(latest_log), encoding="utf-8"
            )
        except OSError:
            pass

    # --- B) Periodic log nagging ---
    nag_message = None

    if latest_log is None:
        # No session log exists
        if not state.get("no_log_reminded"):
            state["no_log_reminded"] = True
            nag_message = (
                f"No session log found. Create one at "
                f"quality_reports/sessions/{today}_description.md "
                f"with: current goal, approach, and key context."
            )
    else:
        current_mtime = latest_log.stat().st_mtime

        # Log was updated since last check → reset counters
        if current_mtime != state.get("last_log_mtime"):
            state["last_log_mtime"] = current_mtime
            state["nag_count"] = 0
            state["responses_since_log_update"] = 0
        else:
            state["responses_since_log_update"] = state.get("responses_since_log_update", 0) + 1
            responses_since = state["responses_since_log_update"]
            nag_count = state.get("nag_count", 0)

            if nag_count < MAX_NAGS_PER_CYCLE:
                # First nag at FIRST_NAG_THRESHOLD, then every RENAG_INTERVAL
                if nag_count == 0 and responses_since >= FIRST_NAG_THRESHOLD:
                    state["nag_count"] = 1
                    nag_message = (
                        f"SESSION LOG REMINDER: {responses_since} responses since last log update. "
                        f"Append 1-3 lines to {latest_log.name} with recent decisions or progress."
                    )
                elif nag_count > 0 and responses_since >= FIRST_NAG_THRESHOLD + nag_count * RENAG_INTERVAL:
                    state["nag_count"] = nag_count + 1
                    nag_message = (
                        f"SESSION LOG REMINDER (repeat {nag_count + 1}/{MAX_NAGS_PER_CYCLE}): "
                        f"{responses_since} responses since last log update. "
                        f"Update {latest_log.name} now."
                    )

    # --- D) MEMORY.md nudge ---
    memory_nudge = None
    if count > 0 and count % MEMORY_NUDGE_INTERVAL == 0:
        mem_path = Path("MEMORY.md")
        if mem_path.exists():
            try:
                current_mem_mtime = mem_path.stat().st_mtime
                start_mem_mtime = state.get("memory_mtime_at_start")
                if start_mem_mtime and current_mem_mtime <= start_mem_mtime:
                    memory_nudge = (
                        "MEMORY.md hasn't been updated this session. "
                        "If you've learned something worth preserving, "
                        "add a [LEARN:category] entry now."
                    )
            except OSError:
                pass

    save_state(state_path, state)

    # Build output — combine messages if needed
    messages = []
    if nag_message:
        messages.append(nag_message)
    if memory_nudge:
        messages.append(memory_nudge)

    if messages:
        # In autonomous mode: write snapshots silently, don't block with nags
        if _utils.is_autonomous_mode():
            # Still write the rolling snapshot (already done above), but suppress nag output
            pass
        else:
            # Use "approve" to deliver reminders without blocking the stop.
            # "block" on Stop events prevents clean exit and causes
            # "Deferred to next session" artifacts in orchestrator loops.
            output = {
                "decision": "approve",
                "reason": "[Stop Checkpoint] " + " | ".join(messages),
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
