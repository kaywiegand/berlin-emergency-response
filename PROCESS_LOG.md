# PROCESS_LOG.md — Berlin Emergency Response

> Projektverlauf und Einstiegspunkt für neue Claude-Sessions.
> Pointer auf Files, keine kopierten Inhalte.

| Feld | Inhalt |
| :--- | :--- |
| Status | S3 Geodaten + App abgeschlossen (Zwischenprüfung offen) |
| Plan | `docs/PLAN.md` |
| Nächster Schritt | `/project-case check`, dann S4 Automatisierung |

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

### 2026-10-08 — S2 dbt-Kern

- Sources + Freshness, 3 Seeds, 6 Staging-, 2 Intermediate-, 6 Mart-Modelle, Macros (`is_within_timegoal`, `safe_pct`, `stg_regional`), Var `timegoal_seconds`. Details: `models/*/schema.yml`, `docs/DATA_DICTIONARY.md`.
- Entscheidung: zwei getrennte Kennzahlen. Offiziell (Regional, 2024–26, mit Hinweis auf Definitionsbruch) und eigene Näherung im Zeitverlauf je Kritikalitätsstufe statt binärem "kritisch". Begründung: BACKLOG 1/2.
- Entscheidung: alte Modellkette, `raw_missions_daily` und App-Abhängigkeit entfernt; App bis S3 defekt (BACKLOG 6).
- Entscheidung: `fct_missions_daily_district` inkrementell über `loaded_at`, `delete+insert` auf `mission_date`; Ingestion ersetzt Jahrespartitionen mit neuem `_loaded_at`.
- Verifiziert: `dbt build` grün (Tests, Singular-Tests), Freshness pass, Rerun ohne Duplikate, manipulierter Regional-Wert lässt `assert_regional_matches_mission_data` rot werden.
- Befunde: Regional-Totals weichen von Mission_Data um bis ~0,3 % ab (Toleranz 1 %). Telefonie-Störung betrifft nur Call-Daten, nicht Einsätze (`seed_events`).
- Nächster Schritt: S3.

### 2026-10-08 — S3 Geodaten + App

- `scripts/fetch_lor.py` (WFS Geoportal Berlin, LOR 2021, CC BY 3.0 DE, vereinfacht), `scripts/export_parquet.py`, `src/app.py` neu auf `app_data/`. Tests: `tests/test_app_data.py` (u. a. AppTest je Kartenebene).
- Entscheidung: Monatsgrain in der App, damit Parquet klein bleibt (tägliche Bot-Commits in S4). Medianen sind nicht additiv, der Export trägt Summen.
- Entscheidung: Plotly-Theme als `wgnd` v0.4.0 (lokal committet, Push offen, BACKLOG 13). Dev-Install mit `uv run --no-sync`.
- Entscheidung: zwei Kennzahlen nebeneinander (offiziell vs. eigene Näherung D/E, ≤ 600 s), Definitionsbruch 2024→2025 sichtbar (Event-Marker aus `seed_events`, Hinweis in der App).
- Befund: LOR-Flächen decken alle 743 Regionen ab; Näherung sinkt 2018–2023 deutlich (BACKLOG 16).
- Nächster Schritt: `/project-case check` als Zwischenprüfung, danach S4.
