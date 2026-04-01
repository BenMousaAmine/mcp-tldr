# Claude System

Sistema di memoria persistente e ottimizzazione per Claude Code.
Riduce il consumo di token, elimina l'esplorazione cieca e mantiene il contesto tra sessioni.

---

## Cosa fa

- **All'avvio** → carica automaticamente l'architettura del progetto e gli errori da evitare
- **Durante il lavoro** → inietta il contesto dell'area su cui stai lavorando
- **A fine sessione** → forza l'aggiornamento della memoria prima di chiudere
- **Dopo ogni modifica** → traccia i file toccati per aggiornare il contesto

---

## Prerequisiti

- [Claude Code](https://claude.ai/code) installato
- [tldr](https://github.com/your-tldr-link) installato (`pip install tldr`)
- [mgrep](https://github.com/your-mgrep-link) configurato come MCP in Claude Code
- Node.js + npx
- Python 3.11+
- `jq` installato (`brew install jq`)

---

## Installazione

```bash
git clone https://github.com/YOUR_USER/claude-system.git
cd claude-system
bash install-claude-system.sh
```

Riavvia Claude Code dopo l'installazione.

---

## Struttura installata

```
~/.claude/
├── CLAUDE.md                  # Istruzioni globali per Claude
├── settings.json              # Hook di Claude Code
├── hooks/
│   ├── session-start.sh       # Carica contesto all'avvio sessione
│   ├── session-stop.sh        # Forza aggiornamento memoria a fine sessione
│   ├── post-tool-use.sh       # Traccia file modificati
│   └── user-prompt-submit.sh  # Inietta context area se rilevante
├── commands/
│   ├── init-project.md        # /init-project
│   ├── sync-arch.md           # /sync-arch
│   ├── add-layer.md           # /add-layer
│   ├── end-session.md         # /end-session
│   └── investigate.md         # /investigate
└── templates/
    ├── ARCHITECTURE.md        # Template architettura progetto
    ├── context-area.md        # Template area investigata
    └── ERRORS.md              # Template errori ricorrenti
```

---

## Primo utilizzo su un progetto

```bash
cd /path/to/your/project
claude  # apri Claude Code
```

Dentro Claude Code:
```
/init-project
```

Claude analizzerà il progetto e creerà `.claude/` con:
- `ARCHITECTURE.md` — mappa del progetto
- `ERRORS.md` — errori da non ripetere
- `context/` — cartella per le aree investigate

---

## Struttura .claude/ nel progetto

```
your-project/
└── .claude/
    ├── ARCHITECTURE.md        # Mappa viva del progetto
    ├── ERRORS.md              # Errori ricorrenti da evitare
    ├── context/
    │   ├── auth.md            # Investigazione area auth
    │   ├── payments.md        # Investigazione area payments
    │   └── [area].md          # Una per ogni area investigata
    ├── .modified-files        # Log file modificati (auto)
    ├── .last-commit           # Ultimo commit (auto)
    └── .session-log           # Log sessioni (auto)
```

---

## Comandi disponibili

| Comando | Quando usarlo |
|---------|---------------|
| `/init-project` | Prima volta in un progetto senza `.claude/` |
| `/sync-arch` | Dopo modifiche strutturali o pull su sotto-progetti |
| `/add-layer [nome]` | Aggiunto nuovo sotto-progetto al monorepo |
| `/end-session` | Per forzare aggiornamento memoria prima di chiudere |
| `/investigate [area]` | Analisi approfondita di un'area da salvare |

---

## Monorepo

Se hai più sotto-progetti in una cartella madre:

```
/my-project/                  # cartella madre (non su git)
├── .claude/
│   ├── ARCHITECTURE.md       # visione 360° globale
│   └── ERRORS.md
├── backend/                  # su git proprio
│   └── .claude/
│       ├── ARCHITECTURE.md   # dettaglio backend
│       └── context/
├── frontend/                 # su git proprio
│   └── .claude/
└── mobile-ios/               # su git proprio
    └── .claude/
```

**Flusso:**
1. Entra nella cartella madre → `/init-project`
2. Per ogni sotto-progetto → `/add-layer`
3. Dopo pull su un sotto-progetto → `/sync-arch`

---

## Come funziona la memoria

### All'avvio sessione
Claude riceve automaticamente nel contesto:
- `ARCHITECTURE.md` del progetto corrente
- `ARCHITECTURE.md` della cartella madre (se esiste)
- `ERRORS.md`

### Durante il lavoro
Se scrivi un prompt che menziona un'area già investigata (es. "auth", "payments"), Claude riceve automaticamente il file `context/[area].md` corrispondente.

### A fine sessione
Claude viene bloccato e invitato a:
1. Aggiornare `context/[area-toccata].md`
2. Aggiornare `ERRORS.md` se ha trovato pattern da evitare
3. Aggiornare `ARCHITECTURE.md` se ha cambiato struttura
4. Chiedere se lanciare `/sync-arch` (se monorepo)

---

## Tool MCP utilizzati

Il sistema usa questi MCP tool se disponibili:

| Tool | Uso |
|------|-----|
| `ripgrep` MCP | Ricerca testuale locale (prima scelta) |
| `tldr_context` | Capire funzione senza leggere file intero |
| `tldr_structure` | Mappa codice senza esplorare directory |
| `tldr_impact` | Chi chiama questa funzione |
| `tldr_semantic` | Ricerca in linguaggio naturale |

---

## Aggiornare il sistema

```bash
cd claude-system
git pull
bash install-claude-system.sh
```

---

## Disinstallare

```bash
# Rimuovi hooks dal settings.json
python3 - << 'EOF'
import json, os
path = os.path.expanduser("~/.claude/settings.json")
with open(path) as f:
    s = json.load(f)
s.pop("hooks", None)
with open(path, "w") as f:
    json.dump(s, f, indent=2)
print("✅ Hooks rimossi")
EOF

# Rimuovi cartelle
rm -rf ~/.claude/hooks
rm -rf ~/.claude/commands
rm -rf ~/.claude/templates
rm ~/.claude/CLAUDE.md
```

---

## Troubleshooting

**Hook non funzionano:**
```bash
# Verifica che gli script siano eseguibili
ls -la ~/.claude/hooks/
chmod +x ~/.claude/hooks/*.sh
```

**`/init-project` non trovato:**
```bash
# Verifica che i commands siano installati
ls ~/.claude/commands/
```

**tldr non trovato:**
```bash
which tldr
# Se non trovato:
pip install tldr
```
