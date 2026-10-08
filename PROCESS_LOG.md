# PROCESS_LOG.md — Berlin Emergency Response

> Projektverlauf und Einstiegspunkt für neue Claude-Sessions.
> Pointer auf Files, keine kopierten Inhalte.

| Feld | Inhalt |
| :--- | :--- |
| Status | S1 Ingestion abgeschlossen |
| Plan | `docs/PLAN.md` |
| Nächster Schritt | S2 dbt-Kern: Sources auf die neuen Raw-Tabellen |

---

## Verlauf

### 2026-10-08 — S0 Fundament

- `.gitignore` bereinigt: `models/`, `profiles.yml` und `seeds/*.csv` werden jetzt versioniert; Daten-Ignores auf `data/` begrenzt.
- Standard-Dateien (CLAUDE, ROADMAP, BACKLOG, PROCESS_LOG, Makefile, `public/`-Skeleton, `tests/`) aus `wgnd-scaffolding` nachgezogen, an dbt-Projekt angepasst. Bestehendes nicht überschrieben.
- Entscheidung: `profiles.yml` committen, weil nur lokaler DuckDB-Pfad. Secrets gehören nie dorthin.
- Entscheidung: kein `src/<paket>/` aus dem Scaffold — Projekt hat `src/app.py` + `src/utils/`.
- Entscheidung: `DE` im Generator nicht in S0 ergänzt, nur im BACKLOG vermerkt.
- Nächster Schritt: S1 `scripts/ingest.py`.

### 2026-10-08 — S1 Ingestion

- `scripts/ingest.py` ersetzt `ingest_raw_data.py` (gelöscht, Fake-Fallback entfällt). Tests: `tests/test_ingest.py` mit lokalem Fixture-Server (`tests/conftest.py`).
- Entscheidung: Raw-Tabellen komplett `VARCHAR`, Typisierung in dbt-Staging. Metaspalten `_partition`, `_source_file`, `_loaded_at`.
- Entscheidung: Idempotenz über Partition (Jahr/Quartal/`all`/`current`), Delete+Insert, alle Dateien erst laden und prüfen, dann eine Transaktion. Fehler lässt DB unberührt.
- Entscheidung: Unbekannte neue Spalten = Warnung, fehlende = Abbruch.
- Befund: Regional-Daten gibt es nur ab 2024 (BACKLOG 9). Alte Tabelle `raw_missions_daily` bleibt bis S2 (BACKLOG 6).
- Nächster Schritt: S2 Sources + Freshness auf `_loaded_at`, Seeds, Staging.
