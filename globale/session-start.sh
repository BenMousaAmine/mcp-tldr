#!/bin/bash
# Hook: SessionStart
# Carica automaticamente il contesto del progetto all'avvio

INPUT=$(cat)
CWD=$(echo "$INPUT" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('cwd',''))" 2>/dev/null)

if [ -z "$CWD" ]; then
  exit 0
fi

CLAUDE_DIR="$CWD/.claude"
CONTEXT=""

# 1. Controlla se esiste ARCHITECTURE.md locale
if [ -f "$CLAUDE_DIR/ARCHITECTURE.md" ]; then
  CONTEXT="$CONTEXT\n## Architettura progetto corrente\n"
  CONTEXT="$CONTEXT$(cat "$CLAUDE_DIR/ARCHITECTURE.md")\n"
fi

# 2. Cerca cartella madre con ARCHITECTURE.md
PARENT=$(dirname "$CWD")
if [ -f "$PARENT/.claude/ARCHITECTURE.md" ]; then
  CONTEXT="$CONTEXT\n## Architettura monorepo (cartella madre)\n"
  CONTEXT="$CONTEXT$(cat "$PARENT/.claude/ARCHITECTURE.md")\n"
fi

# 3. Aggiungi ERRORS.md se esiste
if [ -f "$CLAUDE_DIR/ERRORS.md" ]; then
  CONTEXT="$CONTEXT\n## Errori da NON ripetere\n"
  CONTEXT="$CONTEXT$(cat "$CLAUDE_DIR/ERRORS.md")\n"
fi

# 4. Se non esiste .claude/ avvisa
if [ ! -d "$CLAUDE_DIR" ]; then
  CONTEXT="⚠️ Nessun .claude/ trovato in questo progetto. Lancia /init-project per inizializzare il sistema di memoria."
fi

# Output → viene aggiunto al contesto di Claude
if [ -n "$CONTEXT" ]; then
  echo "$CONTEXT"
fi

exit 0
