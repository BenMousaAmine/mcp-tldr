Sincronizza l'ARCHITECTURE.md della cartella madre leggendo tutti i sotto-progetti.

Esegui questi step:

1. Verifica di essere in una cartella madre (contiene sotto-cartelle con .claude/ARCHITECTURE.md)
   — Se non sei in cartella madre: avvisa e fermati

2. Per ogni sotto-progetto che ha .claude/ARCHITECTURE.md:
   - Leggi stack, struttura, flussi principali
   - Estrai: entry points, API contract, dipendenze verso altri layer

3. Aggiorna .claude/ARCHITECTURE.md della cartella madre:
   - Sezione "Layer collegati": aggiorna tabella con tutti i sotto-progetti
   - Sezione "Flussi principali": aggiorna con flussi cross-layer
   - NON toccare: "Zone protette", "Decisioni architetturali", "Layer aggiunti nel tempo"

4. Mostra diff di cosa hai cambiato (solo le sezioni modificate)
