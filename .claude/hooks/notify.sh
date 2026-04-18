#!/bin/bash
# macOS desktop notification when Claude needs attention.
# Triggers on: permission prompts, idle, auth events.
# Requires: macOS with osascript (standard on all Macs).

INPUT=$(cat)
PYTHON=$(command -v python || command -v python3)
MESSAGE=$(echo "$INPUT" | "$PYTHON" -c "import json,sys; d=json.load(sys.stdin); print(d.get('message','Claude needs attention'))" 2>/dev/null || echo "Claude needs attention")
TITLE=$(echo "$INPUT" | "$PYTHON" -c "import json,sys; d=json.load(sys.stdin); print(d.get('title','Claude Code'))" 2>/dev/null || echo "Claude Code")

# macOS notification
if command -v osascript &>/dev/null; then
    osascript -e "display notification \"$MESSAGE\" with title \"$TITLE\" sound name \"Glass\"" 2>/dev/null
fi

exit 0
