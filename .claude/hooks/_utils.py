#!/usr/bin/env python
"""
Shared utilities for Claude Code hooks.
Import with: sys.path.insert(0, str(Path(__file__).parent)); import _utils
"""
import hashlib
import os
import re
import subprocess
from pathlib import Path


def get_session_dir() -> Path:
    """Return the session-specific directory for state files."""
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
    project_hash = hashlib.md5(project_dir.encode()).hexdigest()[:8]
    session_dir = Path.home() / ".claude" / "sessions" / project_hash
    session_dir.mkdir(parents=True, exist_ok=True)
    return session_dir


def get_project_dir() -> Path:
    """Return the project root directory."""
    return Path(os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd()))


def find_latest_session_log() -> "Path | None":
    """Return the most recently modified session log, or None."""
    for logs_dir in [Path("quality_reports/sessions"), Path("quality_reports/session_logs")]:
        if logs_dir.exists():
            logs = sorted(logs_dir.glob("*.md"), key=lambda p: p.stat().st_mtime, reverse=True)
            if logs:
                return logs[0]
    return None


def find_active_plan() -> "tuple[str | None, str | None]":
    """
    Find the most relevant active plan by status content, not just mtime.

    Priority: IN_PROGRESS > APPROVED > DRAFT > no-explicit-status > COMPLETED
    Within same status tier, sort by mtime (most recent first).
    Git-branch boost: if current branch name appears in filename, bump priority.

    Returns (plan_path_str, current_task_str).
    """
    plans_dir = Path("quality_reports/plans")
    if not plans_dir.exists():
        return None, None

    plans = list(plans_dir.glob("*.md"))
    if not plans:
        return None, None

    # Get current git branch for boost
    current_branch = _get_git_branch()

    STATUS_PRIORITY = {
        "IN_PROGRESS": 0,
        "IN-PROGRESS": 0,
        "APPROVED": 1,
        "DRAFT": 2,
        "FINAL": 1,  # treat FINAL same as APPROVED
    }
    # COMPLETED gets 4 (lowest)
    NO_STATUS = 3
    COMPLETED = 4

    scored_plans = []
    for plan in plans:
        try:
            head = plan.read_text(encoding="utf-8", errors="replace")[:500]
        except OSError:
            continue

        # Extract status from first 500 chars
        status_rank = NO_STATUS
        status_match = re.search(r'\*{0,2}Status\*{0,2}:\*{0,2}\s*(\S+)', head, re.IGNORECASE)
        if status_match:
            status_val = status_match.group(1).strip("*").strip().upper()
            if "COMPLETED" in status_val or "DONE" in status_val:
                status_rank = COMPLETED
            else:
                status_rank = STATUS_PRIORITY.get(status_val, NO_STATUS)

        # Git-branch boost: if branch name appears in filename, subtract 0.5
        branch_boost = 0
        if current_branch and current_branch.lower() in plan.name.lower():
            branch_boost = -0.5

        mtime = plan.stat().st_mtime
        # Sort key: (status_rank + branch_boost, -mtime) — lower is better
        scored_plans.append((status_rank + branch_boost, -mtime, plan, head))

    scored_plans.sort(key=lambda x: (x[0], x[1]))

    if not scored_plans:
        return None, None

    best_plan = scored_plans[0][2]
    best_head = scored_plans[0][3]

    # Extract current task (first unchecked checkbox)
    # Reuse head if it captured the full file; only re-read if truncated
    current_task = None
    if len(best_head) >= 500:
        try:
            content = best_plan.read_text(encoding="utf-8", errors="replace")
        except OSError:
            content = best_head
    else:
        content = best_head
    for line in content.split("\n"):
        if re.match(r"\s*[-*]\s*\[ \]", line):
            current_task = line.strip()
            break

    return str(best_plan), current_task


def find_recent_decisions(max_count: int = 5) -> list:
    """Pull last N decision-tagged lines from the most recent session log."""
    log = find_latest_session_log()
    if not log:
        return []
    decisions = []
    try:
        content = log.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return []
    for line in reversed(content.split("\n")):
        if any(m in line for m in ["Decision:", "Chose:", "→", "DECIDED:", "[LEARN:"]):
            decisions.append(line.strip())
            if len(decisions) >= max_count:
                break
    return decisions


def _get_git_branch() -> str:
    """Return current git branch name, or empty string on failure."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True, text=True, timeout=3
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except (OSError, subprocess.TimeoutExpired):
        pass
    return ""


# --- Memory retrieval helpers ---

_STOPWORDS = frozenset({
    "the", "a", "an", "is", "are", "was", "were", "be", "been", "do", "does",
    "did", "have", "has", "had", "will", "would", "can", "could", "should",
    "may", "might", "i", "me", "my", "we", "our", "you", "your", "it", "its",
    "this", "that", "in", "on", "at", "to", "for", "of", "with", "and", "or",
    "not", "no", "but", "if", "when", "how", "what", "which", "from", "by",
})

_LEARN_PATTERN = re.compile(r'\[LEARN:(\w+)\|P(\d)\|(\d{4}-\d{2}-\d{2})\]\s*(.*)')


def _parse_memory_file(path: Path) -> list:
    """Parse a single memory file into list of entry dicts."""
    entries = []
    try:
        for line in path.read_text(encoding="utf-8").splitlines():
            m = _LEARN_PATTERN.match(line.strip())
            if m:
                entries.append({
                    "category": m.group(1),
                    "priority": int(m.group(2)),
                    "date": m.group(3),
                    "text": m.group(4),
                    "raw": line.strip(),
                })
    except OSError:
        pass
    return entries


def _get_current_stage(project_dir: Path) -> "str | None":
    """Read PIPELINE_STATE.md to determine current stage number."""
    ps_path = project_dir / "PIPELINE_STATE.md"
    try:
        content = ps_path.read_text(encoding="utf-8", errors="replace")[:1000]
        m = re.search(r'(?:Current Stage|Active Stage)[:\s]*(\d)', content, re.IGNORECASE)
        if m:
            return m.group(1)
    except OSError:
        pass
    return None


def parse_memory_entries(project_dir=None) -> list:
    """Parse stage-scoped memory: global.md + current stage memory file.
    Falls back to flat MEMORY.md if stage memory doesn't exist."""
    if project_dir is None:
        project_dir = get_project_dir()

    memory_dir = project_dir / "quality_reports" / "memory"
    global_path = memory_dir / "global.md"

    # If stage-scoped memory exists, use it
    if global_path.exists():
        entries = _parse_memory_file(global_path)
        # Try to load current stage memory
        stage = _get_current_stage(project_dir)
        if stage:
            stage_names = {
                "0": "stage-0-discovery", "1": "stage-1-planning",
                "2": "stage-2-data", "3": "stage-3-analysis",
                "4": "stage-4-writing", "5": "stage-5-review",
                "6": "stage-6-submission",
            }
            stage_file = memory_dir / f"{stage_names.get(stage, 'stage-' + stage)}.md"
            entries.extend(_parse_memory_file(stage_file))
        return entries

    # Fallback: flat MEMORY.md (backward compatible)
    return _parse_memory_file(project_dir / "MEMORY.md")


def tokenize_query(text: str) -> list:
    """Lowercase, strip punctuation, remove stopwords, min length 3."""
    tokens = re.findall(r'[a-z0-9_]+', (text or "").lower())
    return [t for t in tokens if t not in _STOPWORDS and len(t) > 2]


def score_entry(entry_text: str, query_tokens: list) -> int:
    """Keyword score: sum of matched token lengths."""
    text_lower = entry_text.lower()
    return sum(len(t) for t in query_tokens if t in text_lower)


def retrieve_memory(user_message: str, project_dir=None) -> "tuple[list, int]":
    """
    Query-based memory retrieval. Returns (selected_entries, total_count).
    Always includes P1. Keyword-matches P2/P3. Falls back to 3 recent P2s.
    """
    entries = parse_memory_entries(project_dir)
    if not entries:
        return [], 0

    p1 = [e for e in entries if e["priority"] == 1]
    query_tokens = tokenize_query(user_message)

    # Score P2/P3 against query
    matched = []
    if query_tokens:
        scored = []
        for e in entries:
            if e["priority"] == 1:
                continue
            s = score_entry(e["text"], query_tokens)
            if s > 0:
                scored.append((s, e))
        scored.sort(key=lambda x: -x[0])
        matched = [e for _, e in scored]

    # Fallback: 3 most recent P2s if no keyword matches
    if not matched:
        p2s = [e for e in entries if e["priority"] == 2]
        matched = p2s[-3:]

    return p1 + matched, len(entries)


def compute_review_tier() -> "tuple[str, dict]":
    """
    Compute review depth tier from git diff --stat.
    Returns (tier, details) where tier is LIGHT/STANDARD/FULL.
    """
    DOC_EXTS = {".md", ".txt", ".rst", ".json", ".yaml", ".yml", ".toml",
                ".csv", ".tsv", ".bib"}

    total_added = 0
    total_deleted = 0
    files_changed = 0
    new_files = False
    all_docs = True

    # git diff HEAD captures both staged and unstaged changes vs HEAD
    try:
        result = subprocess.run(
            ["git", "diff", "HEAD", "--numstat"],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode != 0:
            return "FULL", {"reason": "git diff failed — defaulting to FULL"}
    except (OSError, subprocess.TimeoutExpired):
        return "FULL", {"reason": "git unavailable — defaulting to FULL"}

    for line in result.stdout.strip().splitlines():
        parts = line.split("\t")
        if len(parts) < 3:
            continue
        added, deleted, filepath = parts[0], parts[1], parts[2]
        a = int(added) if added != "-" else 0
        d = int(deleted) if deleted != "-" else 0
        total_added += a
        total_deleted += d
        files_changed += 1
        ext = Path(filepath).suffix.lower()
        if ext not in DOC_EXTS:
            all_docs = False

    # Check for new untracked files
    try:
        untracked = subprocess.run(
            ["git", "ls-files", "--others", "--exclude-standard"],
            capture_output=True, text=True, timeout=5
        )
        if untracked.returncode == 0 and untracked.stdout.strip():
            new_files = True
            for f in untracked.stdout.strip().splitlines():
                files_changed += 1
                ext = Path(f).suffix.lower()
                if ext not in DOC_EXTS:
                    all_docs = False
    except (OSError, subprocess.TimeoutExpired):
        pass

    total_lines = total_added + total_deleted
    details = {
        "lines_changed": total_lines,
        "files_changed": files_changed,
        "new_files": new_files,
        "all_docs": all_docs,
    }

    # Tier logic
    if files_changed == 0:
        return "LIGHT", {**details, "reason": "no changes detected"}
    if all_docs and total_lines <= 20:
        return "LIGHT", {**details, "reason": "docs/config only, ≤20 lines"}
    if total_lines <= 50 and files_changed <= 2 and not new_files:
        return "STANDARD", {**details, "reason": f"{total_lines} lines, {files_changed} files, no new files"}
    return "FULL", {**details, "reason": f"{total_lines} lines, {files_changed} files, new_files={new_files}"}


def is_autonomous_mode() -> bool:
    """Check if running in autonomous mode (silent hooks)."""
    return os.environ.get("CLAUDE_AUTONOMOUS_MODE", "0") == "1"


def get_git_head() -> str:
    """Return current git HEAD as 'sha message', or empty string."""
    try:
        result = subprocess.run(
            ["git", "log", "--oneline", "-1"],
            capture_output=True, text=True, timeout=3
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except (OSError, subprocess.TimeoutExpired):
        pass
    return ""


# --- Short-term memory (rolling FIFO window) ---

_SHORT_TERM_PATH = Path("quality_reports/memory/short-term.md")
_SHORT_TERM_ENTRY_RE = re.compile(
    r'^\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}) \| ([^\]]+)\] (.+)'
)
_SHORT_TERM_HEADER = (
    "# Short-Term Memory — Rolling Window\n"
    "Auto-maintained. Max 10 entries (FIFO). Do not edit manually.\n"
    "Format: [YYYY-MM-DD HH:MM | session] event: description\n\n---\n"
)


def load_short_term_memory(n: int = 5) -> list:
    """Return last n short-term memory entry lines (chronological, most recent last).
    Returns [] if file missing or no valid entries."""
    try:
        lines = _SHORT_TERM_PATH.read_text(encoding="utf-8").splitlines()
    except OSError:
        return []
    entries = [l for l in lines if _SHORT_TERM_ENTRY_RE.match(l)]
    return entries[-n:] if entries else []


def update_short_term_memory(event_type: str, description: str,
                              session_label: str = None) -> None:
    """Append one entry to short-term memory, then prune to max 10."""
    from datetime import datetime as _dt
    if session_label is None:
        session_label = _dt.now().strftime("%Y-%m-%d")
    # Strip to first line only
    description = description.split("\n")[0].strip()
    timestamp = _dt.now().strftime("%Y-%m-%d %H:%M")
    entry = f"[{timestamp} | {session_label}] {event_type}: {description}"
    try:
        if not _SHORT_TERM_PATH.exists():
            _SHORT_TERM_PATH.parent.mkdir(parents=True, exist_ok=True)
            _SHORT_TERM_PATH.write_text(_SHORT_TERM_HEADER + "\n", encoding="utf-8")
        with open(_SHORT_TERM_PATH, "a", encoding="utf-8") as f:
            f.write(entry + "\n")
        prune_short_term_memory()
    except OSError:
        pass


def prune_short_term_memory(max_entries: int = 10) -> None:
    """Keep at most max_entries entries, dropping oldest (FIFO). No age pruning."""
    try:
        text = _SHORT_TERM_PATH.read_text(encoding="utf-8")
    except OSError:
        return
    lines = text.splitlines(keepends=True)
    # Split into header (lines before first entry) and entries
    header_lines = []
    entry_lines = []
    in_header = True
    for line in lines:
        if in_header and _SHORT_TERM_ENTRY_RE.match(line.rstrip()):
            in_header = False
        if in_header:
            header_lines.append(line)
        else:
            entry_lines.append(line)
    if len(entry_lines) <= max_entries:
        return
    surviving = entry_lines[-max_entries:]
    try:
        _SHORT_TERM_PATH.write_text("".join(header_lines) + "".join(surviving),
                                     encoding="utf-8")
    except OSError:
        pass
