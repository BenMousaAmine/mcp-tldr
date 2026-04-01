Investigazione approfondita di un'area del progetto e salvataggio del risultato.

Uso: /investigate [area] (es. /investigate auth, /investigate payments)

Esegui questi step:

1. Identifica i file rilevanti per l'area usando mgrep e tldr_impact

2. Analizza in profondità:
   - Flusso completo (entry → processing → output)
   - Dipendenze (chi chiama cosa)
   - Pattern usati
   - Punti critici o fragili

3. Crea o aggiorna .claude/context/[area].md con:
   - File coinvolti
   - Come funziona (spiegazione concisa)
   - Decisioni architetturali trovate
   - Eventuali problemi o debito tecnico rilevato

4. Aggiorna .claude/ARCHITECTURE.md se hai scoperto flussi non documentati

5. Mostra summary dell'investigazione
