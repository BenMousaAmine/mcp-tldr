Chiudi la sessione aggiornando tutta la memoria del progetto.

Esegui questi step in ordine:

1. Identifica quali aree hai toccato in questa sessione (file modificati, aree investigate)

2. Per ogni area toccata:
   - Esiste .claude/context/[area].md? → aggiorna
   - Non esiste? → crealo da ~/.claude/templates/context-area.md
   - Aggiungi: decisioni prese, errori trovati, investigazioni fatte

3. Se hai scoperto pattern da evitare o errori ricorrenti:
   - Aggiorna .claude/ERRORS.md

4. Se hai modificato struttura del progetto (nuovi file, nuove cartelle, refactor importante):
   - Aggiorna sezione rilevante in .claude/ARCHITECTURE.md

5. Se esiste cartella madre:
   - Chiedi: "Vuoi che lancio /sync-arch per aggiornare la visione globale?"

6. Mostra summary finale:
   - Cosa hai fatto
   - File .claude/ aggiornati
   - TODO rimasti aperti
