#!/bin/bash
# Hook: UserPromptSubmit
# Se il prompt menziona un'area già investigata, inietta il context file

INPUT=$(cat)

PROMPT=$(echo "$INPUT" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('prompt','').lower())" 2>/dev/null)
CWD=$(echo "$INPUT" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('cwd',''))" 2>/dev/null)

CONTEXT_DIR="$CWD/.claude/context"

if [ ! -d "$CONTEXT_DIR" ]; then
  exit 0
fi

# Controlla se il prompt menziona un'area già investigata
ADDITIONAL_CONTEXT=""

for CONTEXT_FILE in "$CONTEXT_DIR"/*.md; do
  [ -f "$CONTEXT_FILE" ] || continue
  AREA=$(basename "$CONTEXT_FILE" .md)
  
  # Se il prompt contiene il nome dell'area
  if echo "$PROMPT" | grep -qi "$AREA"; then
    ADDITIONAL_CONTEXT="$ADDITIONAL_CONTEXT\n### Context: $AREA\n$(cat "$CONTEXT_FILE")\n"
  fi
done

# Output JSON con context aggiuntivo
if [ -n "$ADDITIONAL_CONTEXT" ]; then
  python3 -c "
import json, sys
context = sys.argv[1]
print(json.dumps({
  'additionalContext': context
}))
" "$ADDITIONAL_CONTEXT"
fi

exit 0
