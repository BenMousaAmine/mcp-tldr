#!/bin/bash
# Hook: Stop
# Aggiorna automaticamente la memoria del progetto a fine sessione

INPUT=$(cat)

# Evita loop infiniti
STOP_ACTIVE=$(echo "$INPUT" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('stop_hook_active', False))" 2>/dev/null)
if [ "$STOP_ACTIVE" = "True" ]; then
  exit 0
fi

CWD=$(echo "$INPUT" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('cwd',''))" 2>/dev/null)

if [ -z "$CWD" ]; then
  exit 0
fi

CLAUDE_DIR="$CWD/.claude"
LOG="$CLAUDE_DIR/.session-log"

# Se non esiste .claude/ non fare niente
if [ ! -d "$CLAUDE_DIR" ]; then
  exit 0
fi

# Salva timestamp fine sessione
mkdir -p "$CLAUDE_DIR"
echo "$(date '+%Y-%m-%d %H:%M') — sessione terminata" >> "$LOG"

# Inietta reminder a Claude tramite stdout (exit 2 = Claude continua)
echo '{
  "decision": "block",
  "reason": "Prima di chiudere: aggiorna .claude/context/[area-toccata].md con decisioni prese e investigazioni fatte. Aggiorna ERRORS.md se hai trovato pattern da evitare. Se esiste cartella madre, chiedi se lanciare /sync-arch. Poi rispondi con summary di cosa hai fatto."
}' 

exit 2
