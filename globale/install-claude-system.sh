#!/bin/bash
# install-claude-system.sh
# Installa il sistema completo Claude in ~/.claude/
# Uso: bash install-claude-system.sh

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "🚀 Installazione sistema Claude"
echo ""

# ─────────────────────────────────────────
# 1. Struttura cartelle
# ─────────────────────────────────────────
mkdir -p ~/.claude/hooks
mkdir -p ~/.claude/templates
mkdir -p ~/.claude/commands
echo -e "${GREEN}✅ Cartelle create${NC}"

# ─────────────────────────────────────────
# 2. CLAUDE.md globale
# ─────────────────────────────────────────
cp "$SCRIPT_DIR/CLAUDE.md" ~/.claude/CLAUDE.md
echo -e "${GREEN}✅ CLAUDE.md globale installato${NC}"

# ─────────────────────────────────────────
# 3. settings.json (hooks)
# ─────────────────────────────────────────
# Se esiste già settings.json, merge invece di sovrascrivere
if [ -f ~/.claude/settings.json ]; then
  echo -e "${YELLOW}⚠️  settings.json esiste già — faccio merge degli hooks${NC}"
  python3 - << 'PYEOF'
import json

with open(os.path.expanduser("~/.claude/settings.json")) as f:
    existing = json.load(f)

with open("settings.json") as f:
    new = json.load(f)

# Merge hooks
existing_hooks = existing.get("hooks", {})
new_hooks = new.get("hooks", {})

for event, handlers in new_hooks.items():
    if event not in existing_hooks:
        existing_hooks[event] = handlers
    else:
        # Aggiungi solo se non già presente
        existing_commands = [h.get("command","") for group in existing_hooks[event] for h in group.get("hooks",[])]
        for handler_group in handlers:
            for h in handler_group.get("hooks", []):
                if h.get("command","") not in existing_commands:
                    existing_hooks[event].append(handler_group)

existing["hooks"] = existing_hooks

with open(os.path.expanduser("~/.claude/settings.json"), "w") as f:
    json.dump(existing, f, indent=2)
PYEOF
else
  cp "$SCRIPT_DIR/settings.json" ~/.claude/settings.json
fi
echo -e "${GREEN}✅ settings.json installato${NC}"

# ─────────────────────────────────────────
# 4. Hook scripts
# ─────────────────────────────────────────
cp "$SCRIPT_DIR/hooks/session-start.sh" ~/.claude/hooks/
cp "$SCRIPT_DIR/hooks/session-stop.sh" ~/.claude/hooks/
cp "$SCRIPT_DIR/hooks/post-tool-use.sh" ~/.claude/hooks/
cp "$SCRIPT_DIR/hooks/user-prompt-submit.sh" ~/.claude/hooks/
chmod +x ~/.claude/hooks/*.sh
echo -e "${GREEN}✅ Hook scripts installati e resi eseguibili${NC}"

# ─────────────────────────────────────────
# 5. Custom commands
# ─────────────────────────────────────────
cp "$SCRIPT_DIR/commands/"*.md ~/.claude/commands/
echo -e "${GREEN}✅ Custom commands installati${NC}"

# ─────────────────────────────────────────
# 6. Template
# ─────────────────────────────────────────
cp "$SCRIPT_DIR/templates/"*.md ~/.claude/templates/
echo -e "${GREEN}✅ Template installati${NC}"

# ─────────────────────────────────────────
# 7. Verifica installazione
# ─────────────────────────────────────────
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${GREEN}✅ Sistema Claude installato${NC}"
echo ""
echo "Struttura creata:"
echo "  ~/.claude/"
echo "  ├── CLAUDE.md              ✅"
echo "  ├── settings.json          ✅"
echo "  ├── hooks/"
echo "  │   ├── session-start.sh   ✅"
echo "  │   ├── session-stop.sh    ✅"
echo "  │   ├── post-tool-use.sh   ✅"
echo "  │   └── user-prompt-submit.sh ✅"
echo "  ├── commands/"
echo "  │   ├── init-project.md    ✅"
echo "  │   ├── sync-arch.md       ✅"
echo "  │   ├── add-layer.md       ✅"
echo "  │   ├── end-session.md     ✅"
echo "  │   └── investigate.md     ✅"
echo "  └── templates/"
echo "      ├── ARCHITECTURE.md    ✅"
echo "      ├── context-area.md    ✅"
echo "      └── ERRORS.md          ✅"
echo ""
echo "Prossimo passo:"
echo "  1. Riavvia Claude Code"
echo "  2. Vai in un progetto"
echo "  3. Lancia: /init-project"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
