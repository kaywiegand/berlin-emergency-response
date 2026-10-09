# PROCESS_LOG.md — Berlin Emergency Response

> Projektverlauf und Einstiegspunkt für neue Claude-Sessions.
> Pointer auf Files, keine kopierten Inhalte.

| Feld | Inhalt |
| :--- | :--- |
| Status | S3 abgeschlossen, S3b (Fragestellung + Notebooks) beginnt |
| Plan | `docs/PLAN.md` |
| Nächster Schritt | `00_introduction` schreiben, dann `01_exploration_<quelle>` |

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

### 2026-10-09 — Scaffold-Basis nachgezogen

- `notebooks/00_introduction.ipynb`, `src/berlin_emergency_response/` (config, settings, notebook, utils, Unterpakete) und `public/index.html` (Platzhalter, wird in S6 generiert) aus `wgnd-scaffolding` übernommen. Entscheidung (Kay): DA/DS-Standard bleibt die Basis, dbt ist die Ergänzung; Notebooks dokumentieren, testen und explorieren.
- Zusätzlich `02_preparation`, `03_analysis`, `04_insights` (Platzhalter mit Standard-Header). Die alten Notebooks `01_exploration`, `02_analysis`, `03_visualization` (Altstand, nicht mehr lauffähig) gelöscht (Kay-Freigabe).
- Anpassung: Paket installierbar (`[tool.uv] package = true`), Docstrings auf Englisch, `PATHS` um `db`, `app_data`, `dbt_models` erweitert, ML-Konstanten entfernt.
- `wgnd` v0.4.0 nach GitHub gepusht (Kay-Freigabe), `uv.lock` auf den Git-Stand aktualisiert; `uv sync` + 17 Tests grün mit der Git-Version (BACKLOG 13 erledigt).

### 2026-10-09 — Neuausrichtung: Notebooks vor App (S3b)

- Entscheidung (Kay): Notebooks sind die Basisarbeit, die App zeigt nur das Ergebnis von `04_insights`. Mein Plan hatte die App in S3 vor der Analyse gebaut; die Ursachen-Fragen (BACKLOG 1, 2, 16) gehören in die Notebooks.
- Neue Leitfrage: Faktoren, die mit der Antwortzeit zusammenhängen, und wo/wann die Hilfsfrist verfehlt wird; Zusammenhänge statt Ursachen (`docs/CONCEPT.md` Abschnitt 7).
- Notebook-Plan: `00_introduction`, `01_exploration_<quelle>`, `02_preparation`, `03_analysis_<dimension>`, `04_insights` → `app_data/insights.json`. Medallion: raw = Bronze, stg/int = Silver, fct/dim = Gold.
- Anreicherung Stufe 1 (Feiertage/Ferien, Wetter) nach dem ersten EDA-Durchlauf; Stufe 2 später. Politik nur als belegte Annotation.
- Alte Notebooks gelöscht. `BACKLOG.md` neu geschrieben, weil ein Regex-Ersetzen früher Zeilen verschmolzen hatte; Inhalt unverändert bis auf Zahlen-Bereinigung (Review-Finding).

### 2026-10-09 — 00_introduction geschrieben

- `notebooks/00_introduction.ipynb`: Facts, Fragestellung mit Dimensionen/Vermutungen/Grenzen, Quellen-Tabelle (Inhalt, Warum, Wichtig), Antwortzeit vs. Hilfsfrist, Medallion, dbt-Komponenten (Wie/Warum), Notebook-Map; Setup-Zelle zeigt Zeilen je Schicht live aus DuckDB. `make notebooks` führt alle Notebooks aus.
- Befund: Die DuckDB enthielt noch Objekte der in S2 entfernten Modelle (`fct_missions_daily`, `int_missions_daily_enhanced`, `stg_missions_daily`); dbt löscht entfernte Modelle nicht. Manuell gelöscht.
- Offen: Bedeutung der `mission_count_rd1`–`rd5` und `KV_Data` nicht geprüft, deshalb nicht erklärt.
- Nächster Schritt: `01_exploration_missions` (mit `wgnd.inspect`), dann die weiteren Quellen.
