# PROCESS_LOG.md — Berlin Emergency Response

> Projektverlauf und Einstiegspunkt für neue Claude-Sessions.
> Pointer auf Files, keine kopierten Inhalte.

| Feld | Inhalt |
| :--- | :--- |
| Status | S0 Fundament in Arbeit |
| Plan | `docs/PLAN.md` |
| Nächster Schritt | S0 abschließen, dann S1 Ingestion |

---

## Verlauf

### 2026-10-08 — S0 Fundament

- `.gitignore` bereinigt: `models/`, `profiles.yml` und `seeds/*.csv` werden jetzt versioniert; Daten-Ignores auf `data/` begrenzt.
- Standard-Dateien (CLAUDE, ROADMAP, BACKLOG, PROCESS_LOG, Makefile, `public/`-Skeleton, `tests/`) aus `wgnd-scaffolding` nachgezogen, an dbt-Projekt angepasst. Bestehendes nicht überschrieben.
- Entscheidung: `profiles.yml` committen, weil nur lokaler DuckDB-Pfad. Secrets gehören nie dorthin.
- Entscheidung: kein `src/<paket>/` aus dem Scaffold — Projekt hat `src/app.py` + `src/utils/`.
- Entscheidung: `DE` im Generator nicht in S0 ergänzt, nur im BACKLOG vermerkt.
- Nächster Schritt: S1 `scripts/ingest.py`.
