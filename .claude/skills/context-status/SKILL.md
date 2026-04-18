---
name: context-status
description: Show session health — context usage, active plan, preservation state.
allowed-tools: ["Bash", "Read", "Glob"]
---

# /context-status — Session Health Check

## Steps

1. **Check context monitor cache:**
```bash
ls ~/.claude/sessions/*/context-monitor-cache.json 2>/dev/null | head -3
```
Read the most recent cache file for current call count estimate.

2. **Find active plan:**
```bash
ls -lt quality_reports/plans/*.md 2>/dev/null | head -3
```

3. **Find session log:**
```bash
ls -lt quality_reports/sessions/*.md 2>/dev/null | head -1
```

4. **Check hooks configured:**
```bash
cat ~/.claude/settings.json | python -c "import json,sys; d=json.load(sys.stdin); print('Hooks:', list(d.get('hooks',{}).keys()))" 2>/dev/null
```

5. **Report in this format:**

```
Session Status
────────────────────────────────────
Context:    ~XX% estimated (N tool calls × ~4k tokens / 200k window)
Compact?:   [approaching | not imminent]

Active Plan
File:   quality_reports/plans/YYYY-MM-DD_description.md
Status: [APPROVED / IN_PROGRESS / none found]
Task:   [current unchecked task or "—"]

Session Log
File:   quality_reports/sessions/YYYY-MM-DD_description.md
Last:   [time since last update, or "—"]

Hooks
PreCompact:   [configured | MISSING]
Stop (log):   [configured | MISSING]
PostCompact:  [configured | MISSING]

Preservation
Plans on disk:   [Y files]
Session logs:    [Y files]
MEMORY.md:       [exists | MISSING]
```
