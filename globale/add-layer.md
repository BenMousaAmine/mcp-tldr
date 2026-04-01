Aggiunge un nuovo layer/sotto-progetto alla visione globale del monorepo.

Uso: /add-layer (poi Claude chiede nome e path)

Esegui questi step:

1. Chiedi se non forniti:
   - Nome del layer (es. "mobile-android")
   - Path relativo dalla cartella madre (es. "./android-app")

2. Vai nel path indicato e analizza:
   - Rileva stack
   - tldr_tree + tldr_structure
   - Identifica entry points e API utilizzate

3. Crea .claude/ nel nuovo layer:
   - ARCHITECTURE.md compilato con dati reali
   - ERRORS.md vuoto

4. Aggiorna .claude/ARCHITECTURE.md della cartella madre:
   - Aggiungi riga in "Layer collegati"
   - Aggiorna "Flussi principali" se il nuovo layer interagisce con gli esistenti
   - Aggiungi riga in "Layer aggiunti nel tempo" con data e motivo

5. Mostra summary di cosa hai fatto
