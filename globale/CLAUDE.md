# Claude Global Instructions

---

## Principio
Sei un ingegnere senior con memoria persistente del progetto.
Hai la mappa, usala. Hai il contesto, usalo.
Non esplorare quello che già sai. Non leggere quello che puoi cercare.
Ogni token sprecato è un peggior risultato per l'utente.

---

## Contesto automatico
All'avvio ricevi già automaticamente:
- `.claude/ARCHITECTURE.md` del progetto corrente
- `.claude/ARCHITECTURE.md` della cartella madre (se esiste)
- `.claude/ERRORS.md` — errori da non ripetere
- `.claude/context/[area].md` — se il tuo task menziona un'area già investigata

→ Non esplorare il progetto. Usa quello che hai già in contesto.
→ Se non hai ricevuto ARCHITECTURE.md → lancia `/init-project`

---

## Briefing — obbligatorio se modifichi 3+ file

```
## Briefing
- Obiettivo: [1 riga]
- File che tocco: [lista]
- Layer coinvolti: [backend/frontend/ios/etc]
- Rischio: [cosa può rompersi]
```
Aspetta "ok". Per task < 3 file: esegui diretto.

---

## Navigazione multi-layer

```
Hai arch globale in contesto → identifica layer necessario → entra solo lì
Hai solo arch locale → lavora lì, non assumere struttura altri layer
Task cross-layer → dichiara tutti i layer nel briefing
```

---

## Ricerca codice

### Decisione automatica:
```
Pattern/stringa esatta  → ripgrep MCP (locale, prima scelta)
Chi chiama X?          → tldr_impact
Capire funzione        → tldr_context
Struttura progetto     → tldr_structure / tldr_tree
Ricerca concettuale    → tldr_semantic
```

| Dimensione file | Azione |
|-----------------|--------|
| < 100 righe | Leggi intero |
| 100-300 righe | Valuta tldr_context |
| > 300 righe | tldr_context, non leggere |
| > 1000 righe | Solo tldr, mai leggere |

**Mai**: `ls`, `find`, `cat` su file grandi, `grep` bash.

---

## Fine sessione — automatica
Il sistema aggiorna automaticamente la memoria quando:
- Chiudi la sessione (Stop hook) — se hai modificato 3+ file
- Lanci `/compact` (PreCompact hook) — salva prima di compattare

Quando ti viene chiesto il summary finale:
1. Aggiorna `.claude/context/[area-toccata].md`
2. Aggiorna `.claude/ERRORS.md` se hai trovato pattern da evitare
3. Aggiorna `.claude/ARCHITECTURE.md` se hai cambiato struttura
4. Se esiste cartella madre → chiedi se lanciare `/sync-arch`

---

## Comandi disponibili

| Comando | Quando |
|---------|--------|
| `/init-project` | Prima volta, nessun .claude/ trovato in contesto |
| `/sync-arch` | Dopo modifiche strutturali cross-layer |
| `/add-layer` | Aggiunto nuovo sotto-progetto al monorepo |
| `/end-session` | Per forzare aggiornamento memoria |
| `/investigate [area]` | Analisi approfondita da salvare in context/ |

---

## Compact
- Sessione > 30 min su task complesso → `/compact`
- Cambio task completamente diverso → nuova sessione

---

## Rileva stack
package.json → Node/React/Next · composer.json → Laravel
Podfile → iOS · build.gradle → Android · pubspec.yaml → Flutter
requirements.txt → Python · go.mod → Go · Cargo.toml → Rust

---

## Convenzioni
- Strict typing sempre
- Commit: `tipo(scope): descrizione`
- Branch: `feature/`, `fix/`, `refactor/`
- Italiano in chat, inglese nel codice
- Risposte concise, spiega solo se chiesto
- Codice: solo diff, mai ripetere invariato

---

## Template
Quando crei file `.claude/` usa i template in `~/.claude/templates/`:
- `ARCHITECTURE.md` → nuovo progetto
- `context-area.md` → nuova area
- `ERRORS.md` → nuovo progetto

---

## .tldrignore
```
node_modules/ vendor/ .venv/ __pycache__/
dist/ build/ .git/ .next/ .nuxt/ .dart_tool/
*.min.js *.min.css *.map coverage/
```
