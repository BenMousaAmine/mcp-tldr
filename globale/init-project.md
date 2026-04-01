Analizza il progetto corrente e inizializza il sistema .claude/.

Esegui questi step in ordine:

1. Controlla se esiste già .claude/ARCHITECTURE.md — se sì, chiedi conferma prima di sovrascrivere

2. Rileva stack leggendo: package.json, composer.json, Podfile, build.gradle, requirements.txt, pubspec.yaml

3. Mappa la struttura usando OBBLIGATORIAMENTE questi tool MCP nell'ordine:
   - `tldr_tree` per vedere l'albero file (MAI usare ls, find o bash per listare directory)
   - `tldr_structure` con il lang rilevato per vedere classi e funzioni
   - `tldr_warm` per indicizzare il progetto prima di altre query tldr

4. Determina il tipo di progetto:
   - monorepo-root: contiene più sotto-cartelle con stack diversi
   - backend: solo API/server
   - frontend: solo web app
   - mobile-ios: solo iOS
   - mobile-android: solo Android
   - fullstack: frontend + backend nella stessa cartella

5. Crea .claude/ con questi file usando i template in ~/.claude/templates/:
   - ARCHITECTURE.md (compilato con dati reali del progetto)
   - ERRORS.md (vuoto ma pronto)
   - context/ (cartella vuota)

6. Se monorepo-root: per ogni sotto-progetto rilevato, chiedi "Vuoi che inizializzo anche [nome]?"

7. Mostra summary di cosa hai creato e chiedi: "Ci sono aree critiche da investigare subito per creare il primo context file?"