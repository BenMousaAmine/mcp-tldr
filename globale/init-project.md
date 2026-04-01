Analizza il progetto corrente e inizializza il sistema .claude/.

Esegui questi step in ordine:

1. Controlla se esiste già .claude/ — se sì, chiedi conferma prima di sovrascrivere

2. Rileva stack leggendo: package.json, composer.json, Podfile, build.gradle, requirements.txt, pubspec.yaml

3. Usa tldr_tree e tldr_structure per mappare la struttura

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
