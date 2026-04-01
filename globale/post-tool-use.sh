#!/bin/bash
# Hook: PostToolUse matcher: Edit|Write|MultiEdit
# Traccia file modificati per sapere quali context aggiornare

INPUT=$(cat)

FILE_PATH=$(echo "$INPUT" | python3 -c "
import json, sys
d = json.load(sys.stdin)
ti = d.get('tool_input', {})
print(ti.get('file_path', ti.get('path', '')))
" 2>/dev/null)

if [ -z "$FILE_PATH" ]; then
  exit 0
fi

CWD=$(echo "$INPUT" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('cwd',''))" 2>/dev/null)
CLAUDE_DIR="$CWD/.claude"

if [ ! -d "$CLAUDE_DIR" ]; then
  exit 0
fi

# Logga file modificato
MODIFIED_LOG="$CLAUDE_DIR/.modified-files"
echo "$(date '+%H:%M') $FILE_PATH" >> "$MODIFIED_LOG"

# Mantieni solo ultime 50 righe
tail -50 "$MODIFIED_LOG" > "$MODIFIED_LOG.tmp" && mv "$MODIFIED_LOG.tmp" "$MODIFIED_LOG"

exit 0
