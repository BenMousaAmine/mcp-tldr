# Errori ricorrenti — [PROJECT NAME]
> Leggi SEMPRE prima di iniziare un task.
> Aggiornato: [DATA]

---

## Errori architetturali
> Decisioni sbagliate già prese e corrette
- ❌ [errore] → ✅ [soluzione corretta]

---

## Errori di pattern
> Usi sbagliati di framework o librerie
- ❌ [es. usare DB::table() invece di Eloquent] → ✅ [usare Model con cast]
- ❌ [es. logica nel Controller] → ✅ [logica nel Service]

---

## File pericolosi
> File che sembrano semplici ma nascondono dipendenze critiche
| File | Perché è pericoloso | Come toccarlo |
|------|--------------------|--------------| 
| `[path]` | [motivo] | [procedura sicura] |

---

## Sequenze obbligatorie
> Alcune operazioni vanno fatte in ordine preciso
- Per [operazione]: prima [A] poi [B] poi [C]

---

## Mai fare
- Mai modificare migration esistenti — crea sempre nuova migration
- Mai cambiare API response structure senza aggiornare frontend
- [regola specifica del progetto]
