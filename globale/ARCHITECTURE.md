# Architecture — [PROJECT NAME]
> Auto-generato da Claude. Aggiornato: [DATA]
> Tipo: [monorepo-root | backend | frontend | mobile-ios | mobile-android | fullstack]

---

## Stack
- **Runtime**: [es. PHP 8.2, Node 20, Python 3.12, Swift 5.9]
- **Framework**: [es. Laravel 11, Next.js 15, FastAPI]
- **DB**: [es. PostgreSQL su RDS, Supabase, SQLite]
- **Storage**: [es. S3, Cloudinary]
- **Deploy**: [es. EC2, Vercel, App Store]

---

## Struttura layer
```
[albero cartelle principali — max 2 livelli]
```

---

## Layer collegati
> (solo se cartella madre esiste)
| Layer | Path | Ruolo |
|-------|------|-------|
| backend | ../backend/ | API REST |
| frontend | ../frontend/ | Web app |
| ios | ../ios/ | App mobile |

---

## Flussi principali
> Scrivi solo i flussi critici, max 5
- **Auth**: [entry point] → [controller] → [service] → [DB]
- **[Feature principale]**: [percorso]

---

## Entry points
- API base: `[url o file routes]`
- Auth: `[file o endpoint]`
- Config env: `[file .env o config]`

---

## Zone protette — NON TOCCARE senza conferma
- [ ] `[file o cartella]` — motivo
- [ ] Migration esistenti — mai modificare, solo aggiungere
- [ ] API contract pubbliche — breaking change richiede discussione

---

## Dove mettere le mani
| Task | Dove iniziare |
|------|---------------|
| Nuova API endpoint | `[path controller]` + `[path routes]` |
| Nuovo componente UI | `[path components]` |
| Nuova tabella DB | `[path migrations]` + `[path models]` |
| Nuova schermata mobile | `[path screens]` |

---

## Decisioni architetturali
- [data]: [decisione presa e perché]

---

## Layer aggiunti nel tempo
> (solo per cartella madre)
- [data]: aggiunto [layer] — [motivo]
