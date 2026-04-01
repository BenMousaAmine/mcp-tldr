#!/bin/bash
# Hook: Stop
# Aggiorna memoria solo a fine sessione vera (non dopo ogni risposta)

INPUT=$(cat)

# Evita loop infiniti
STOP_ACTIVE=$(echo "$INPUT" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('stop_hook_active', False))" 2>/dev/null)
if [ "$STOP_ACTIVE" = "True" ]; then
  exit 0
fi

CWD=$(echo "$INPUT" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('cwd',''))" 2>/dev/null)
CLAUDE_DIR="$CWD/.claude"

if [ ! -d "$CLAUDE_DIR" ]; then
  exit 0
fi

# Conta file modificati in questa sessione
MODIFIED_LOG="$CLAUDE_DIR/.modified-files"
if [ ! -f "$MODIFIED_LOG" ]; then
  exit 0
fi

MODIFIED_COUNT=$(wc -l < "$MODIFIED_LOG" | tr -d ' ')

# Aggiorna solo se ha modificato almeno 3 file — altrimenti troppo rumore
if [ "$MODIFIED_COUNT" -lt 3 ]; then
  exit 0
fi

# Svuota il log per la prossima sessione
> "$MODIFIED_LOG"

# Chiedi a Claude di fare il summary
echo '{
  "decision": "block",
  "reason": "Hai modificato diversi file in questa sessione. Prima di chiudere: aggiorna .claude/context/[area-toccata].md con decisioni prese. Aggiorna ERRORS.md se hai trovato pattern da evitare. Rispondi con un summary breve di cosa hai fatto."
}'

exit 2