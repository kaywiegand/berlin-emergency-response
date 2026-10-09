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
- Geklärt in `01_exploration_daily`: `rd1`–`rd5` sind Notfallkategorien (RD1/RD2 laut BF "critical"); `KV_Data` bezieht sich auf die Kassenärztliche Vereinigung (Feldbeschreibung).
- Nächster Schritt: `01_exploration_missions` (mit `wgnd.inspect`), dann die weiteren Quellen.

### 2026-10-09 — 01_exploration_missions

- Notebook mit Struktur, Missing, Duplikaten, Kategorien, Antwortzeit, Zeit und Fazit (Inhalt, Nutzen, Grenzen, Beobachtungen, offene Fragen). Profil-Funktionen laufen auf fester Stichprobe (Seed 42), Anteile per SQL auf der Gesamtmenge.
- Befund (Details im Notebook): Antwortzeit fehlt systematisch (nach Einsatztyp und Stufe), die Dispatch-Stufe ist über die Jahre nicht stabil (Codeabdeckung, Stufenmix) — stützt die Vermutung hinter BACKLOG 16. Tippfehler `RTW` mit Backtick in `units_first_type`.
- Nächster Schritt: `01_exploration_daily` (inklusive Bedeutung von `mission_count_rd1`–`rd5`).

### 2026-10-09 — 01_exploration_daily, _regional, _turnout, _geo

- Vier Notebooks mit Struktur, Profil, Verteilungen, Abgleich und Fazit (Inhalt, Nutzen, Grenzen, Beobachtungen, offene Fragen). Alle mit gespeicherten Outputs, ohne Fehler.
- Kernbefund Definitionsbruch: `mission_count_ems_critical` entspricht bis 2024 einem breiten Begriff (rund RD1 bis RD4), 2026 nahe RD1 plus RD2; ein zweiter Beleg sind die RTW-Alarmierungen in `Turnout_Times` (Rückgang 2025). Muster zwischen Regionen bleiben stabil (Rangkorrelation hoch), Niveaus nicht vergleichbar.
- Kernbefund Raum: Quote und Antwortzeit hängen mit Abstand zum Zentrum und Einsatzdichte zusammen (Rangkorrelation rund 0,5). Wachen-Koordinaten fehlen noch (Anreicherung Stufe 2).
- Kernbefund Daten: sieben Tage fehlen in der Tagesreihe (alle 2026) und erklären deren Abweichung zu den Einzeleinsätzen; die Regionaldatei 2025 ist etwas kleiner als die anderen Quellen; Prognoseräume sind 58 (Plan korrigiert).
- Nächster Schritt: `02_preparation` (Pipeline im Detail, Entscheidungen aus den Fazits: Backtick, `is_reliable`, `seed_stations`, Geometrie-Merkmale, Lückentest).

### 2026-10-09 — Feuerwehr-Standorte als neue Quelle

- Anlass (Kay): Datensatz "Feuerwehr Standorte und Einsatzbereiche" auf daten.berlin.de war nicht berücksichtigt. Prüfung: WFS am Geoportal liefert 102 Standorte (Punkte) und 6 Einsatzbereiche, dl-de-zero-2.0; `wach_nr` passt zu `wache_nummer` aus `Turnout_Times` (77 von 80).
- Neu: `scripts/fetch_stations.py` (`make stations`), `seeds/seed_stations.csv` mit Tests, `app_data/geo/fire_operational_areas.geojson`, `01_exploration_stations`, Zeile in `00_introduction`, `relationships`-Test von `stg_turnout_times` (`warn`).
- Befund: Abstand zur nächsten Wache hängt stärker mit Quote und Antwortzeit zusammen als der Abstand zum Zentrum (abhängig von der Wachen-Menge; Details im Notebook). Annahme "Freiwillige Feuerwehr stellt keinen RTW" trägt nicht, FF-Standorte haben RTW-Alarmierungen.
- Zeitpunkt: Der Datensatz hätte bei der Quellenprüfung in S0/S1 auffallen müssen (der Plan nannte Wachen-Koordinaten als offen).

### 2026-10-09 — Rückmeldungen Kay: Einsatzarten, BF-Diagramme, Einsatzcodes

- Fragen: Gelten für Rettungsdienst, Brand, technische Hilfe dieselben Regeln? Differenzieren die EDA-Notebooks genug? BF-Diagramme sollen ins Ergebnis. Werden die Einsatzcodes berücksichtigt? Phase-2-Quellen vermerkt (`docs/PLAN.md`).
- Befund: Die BF-Seite dokumentiert den Stichtag der Notfallkategorien (25.03.2025); in unserer Tagesreihe springt der Anteil "kritisch" an exakt diesem Tag von rund 96 % auf rund 69 % (danach rund 60 %). `seed_events` entsprechend korrigiert (verifiziert).
- Befund: RD1+RD2 bleibt in der Tagesreihe über den Stichtag hinweg bei rund der Hälfte der RD-Einsätze und ist damit die vergleichbare Grundgesamtheit; die Annahme "Stufe D/E als kritisch" ist zu eng (C/D/E liegt volumenmäßig näher). Notebooks `01_exploration_daily`/`_regional`/`_missions` und die App-Texte sind nach der Feedback-Runde anzupassen.
- Befund: Einsatzcodes-Tabelle der BF (AMPDS, Stand 21.05.2026) ist noch nicht eingebunden; `seed_dispatch_codes` stammt aus Mission_Data (BACKLOG 26).
- Offen aus dem Dialog: dbt-Schwelle 600 s gilt für alle Einsatzgruppen (BACKLOG 25).
- Entscheidung (Kay): Die unterschiedlichen Fristen je Einsatzart gehören in die README; Gesamtbetrachtungen werden immer nach Einsatzart aufgeschlüsselt, die Aufteilung ist Pflicht. Umgesetzt in README ("Fristen und Schutzziele"), CLAUDE.md (Konvention), CONCEPT; Umsetzung in Notebooks/Marts/App steht aus (BACKLOG 24, 25).
- Beleg (Kay-Recherche, geprüft gegen die BF-Seite "Berliner Feuerwehr in Zahlen"): Brand Frist 15 min (Soll A 90 %, B 50 %), Notfallrettung Frist 10 min (Soll 90 %); **technische Hilfeleistung: nur die durchschnittlich erreichte Hilfsfrist, keine Frist, kein Soll.** Die KI-Zusammenfassungen aus der Recherche (technische Hilfe gleich 15 min, Klasse A 8 min) stehen so nicht auf der BF-Seite und gelten als unbelegt. Dieselbe Seite nennt 18 Rettungswachen auf FF-Standorten; das erklärt RTW-Alarmierungen an `FF`-Standorten in den Turnout-Daten.
