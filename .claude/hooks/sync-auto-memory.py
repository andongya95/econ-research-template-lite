#!/usr/bin/env python
"""
Stop hook: syncs a compact session summary to Claude Code's auto-memory directory.
Writes to ~/.claude/projects/<slug>/memory/MEMORY.md so the next session's system
prompt includes key state. Runs alongside stop-checkpoint.py for resilience.
Cross-platform (Windows/macOS/Linux).
"""
import json
import os
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import _utils


def project_dir_to_slug(project_dir: str) -> str:
    """
    Deterministic conversion of a project directory path to a Claude Code slug.
    Claude Code slug format: drive letter stripped of colon, then all separators
    become dashes. E.g.:
      /Users/alice/project  → -Users-alice-project
      D:\\Dropbox\\project   → D--Dropbox-project  (colon removed, \\ → -)
    """
    slug = project_dir.replace(":", "").replace("\\", "-").replace("/", "-")
    return slug


def find_auto_memory_dir() -> "Path | None":
    """
    Find the auto-memory directory for this project using deterministic
    slug conversion from CLAUDE_PROJECT_DIR.
    """
    claude_projects = Path.home() / ".claude" / "projects"
    if not claude_projects.exists():
        return None

    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
    slug = project_dir_to_slug(project_dir)

    # Primary: exact slug match
    exact_dir = claude_projects / slug / "memory"
    if exact_dir.exists():
        return exact_dir

    # Fallback: scan for directories whose name matches the slug exactly
    # (handles edge cases where the slug directory exists but memory/ hasn't
    # been created yet, or minor platform normalization differences)
    for candidate in claude_projects.iterdir():
        if not candidate.is_dir():
            continue
        if candidate.name == slug:
            memory_dir = candidate / "memory"
            if memory_dir.exists():
                return memory_dir

    return None


def main():
    # Read hook input
    try:
        hook_input = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        hook_input = {}

    if hook_input.get("stop_hook_active", False):
        sys.exit(0)

    auto_memory_dir = find_auto_memory_dir()
    if not auto_memory_dir:
        sys.exit(0)

    # Read last-session-summary.json for state
    session_dir = _utils.get_session_dir()
    summary_path = session_dir / "last-session-summary.json"
    summary = None
    if summary_path.exists():
        try:
            with open(summary_path, encoding="utf-8") as f:
                summary = json.load(f)
        except (OSError, json.JSONDecodeError):
            pass

    if not summary:
        sys.exit(0)

    # Build compact auto-memory content
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [
        f"# Auto-Memory (updated: {timestamp})",
        "",
        "## Last Session State",
    ]

    if summary.get("active_plan"):
        lines.append(f"- **Plan:** {summary['active_plan']}")
    if summary.get("latest_session_log"):
        lines.append(f"- **Log:** {summary['latest_session_log']}")
    if summary.get("git_head"):
        lines.append(f"- **Git HEAD:** {summary['git_head']}")
    if summary.get("response_count"):
        lines.append(f"- **Responses:** {summary['response_count']}")

    decisions = summary.get("recent_decisions", [])
    if decisions:
        lines.append("")
        lines.append("## Recent Decisions")
        for d in decisions[:5]:
            lines.append(f"- {d}")

    # Read current task from summary
    if summary.get("current_task"):
        lines.append("")
        lines.append("## Active Tasks")
        lines.append(f"- {summary['current_task']}")

    lines.append("")

    # Write to auto-memory
    memory_file = auto_memory_dir / "MEMORY.md"
    try:
        memory_file.write_text("\n".join(lines), encoding="utf-8")
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
