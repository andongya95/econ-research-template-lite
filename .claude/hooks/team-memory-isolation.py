#!/usr/bin/env python
"""
PreToolUse hook: enforces memory isolation for research team coauthor agents.

Blocks Read/Glob/Grep/Bash calls that target another coauthor's memory or output
file. The agent's own role is detected from the CLAUDE_AGENT_ROLE environment
variable (set by the PI coordinator in the dispatch prompt via env).

If CLAUDE_AGENT_ROLE is not set, the hook is a no-op (non-team context).
"""
import json
import os
import sys

TEAM_MEMORY_DIR = "quality_reports/team/memory/"
TEAM_ROUND_DIR = "quality_reports/team/round-"

CORE_ROLES = ["econometrician", "paper-writer", "theorist"]


def detect_coauthor_roles():
    """Discover all coauthor roles from existing memory files.

    Scans quality_reports/team/memory/ for *-memory.md files to support
    dynamically created specialist agents alongside the core team.
    """
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
    memory_dir = os.path.join(project_dir, "quality_reports", "team", "memory")
    if not os.path.isdir(memory_dir):
        return list(CORE_ROLES)

    roles = []
    for f in os.listdir(memory_dir):
        if f.endswith("-memory.md"):
            role = f[: -len("-memory.md")]
            if role and role != "pi":
                roles.append(role)

    # Always include core roles even if memory files don't exist yet
    for core in CORE_ROLES:
        if core not in roles:
            roles.append(core)
    return roles


def normalize_path(p: str) -> str:
    """Normalize to forward slashes for consistent matching."""
    return p.replace("\\", "/")


def check_path_violation(normalized: str, role: str):
    """Check a normalized path string for team memory isolation violations.

    Returns a block result dict if a violation is found, or None if the path is allowed.
    """
    needs_role_check = (
        TEAM_MEMORY_DIR in normalized or TEAM_ROUND_DIR in normalized
    )
    if not needs_role_check:
        return None

    all_roles = detect_coauthor_roles()

    # Check 1: Block reading other coauthors' memory files
    if TEAM_MEMORY_DIR in normalized:
        own_memory = f"{role}-memory.md"
        # Allow reading own memory
        if own_memory in normalized:
            return None
        # Block reading any other coauthor's memory
        for other_role in all_roles:
            if other_role != role and f"{other_role}-memory.md" in normalized:
                return {
                    "decision": "block",
                    "reason": (
                        f"Memory isolation violation: {role} cannot read "
                        f"{other_role}'s memory file. Each coauthor reads only "
                        f"their own memory. See research-team-protocol.md."
                    ),
                }

    # Check 2: Block reading other coauthors' output files in round dirs
    if TEAM_ROUND_DIR in normalized:
        for other_role in all_roles:
            if other_role != role and f"{other_role}-output.md" in normalized:
                return {
                    "decision": "block",
                    "reason": (
                        f"Memory isolation violation: {role} cannot read "
                        f"{other_role}'s output file. The PI curates what "
                        f"information flows between coauthors. See "
                        f"research-team-protocol.md."
                    ),
                }

    return None


def main():
    role = os.environ.get("CLAUDE_AGENT_ROLE", "").strip().lower()

    # No role set → not in team context, allow everything
    if not role:
        return

    # PI reads everything
    if role == "pi-coordinator":
        return

    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return

    tool_name = data.get("tool_name", "")
    tool_input = data.get("tool_input", {})

    # --- Bash tool: check the command string for team memory paths ---
    if tool_name == "Bash":
        command = tool_input.get("command", "")
        if not command:
            return

        # Normalize the command string for consistent matching
        normalized_cmd = normalize_path(command)

        # Also check for file:// URL bypass attempts
        # Strip file:// prefixes so underlying paths are checked
        normalized_cmd_with_urls = normalized_cmd.replace("file://", "")

        for check_str in (normalized_cmd, normalized_cmd_with_urls):
            violation = check_path_violation(check_str, role)
            if violation:
                json.dump(violation, sys.stdout)
                return
        return

    # --- Read/Glob/Grep: check the file path ---
    # Try tool_input first (Claude Code wraps), then top-level (direct/test format)
    file_path = (tool_input.get("file_path") or tool_input.get("path")
                 or data.get("file_path") or data.get("path") or "")
    if not file_path:
        return

    # Resolve symlinks before normalization to prevent symlink bypass
    file_path = os.path.realpath(file_path)
    normalized = normalize_path(file_path)

    violation = check_path_violation(normalized, role)
    if violation:
        json.dump(violation, sys.stdout)
        return


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
