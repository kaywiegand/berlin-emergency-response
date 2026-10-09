# PLAN — Berlin Emergency Response

> Doppelziel: Portfolio-Case (Analytics Engineering) und dbt-Zertifizierungsvorbereitung mit allen Komponenten.
> Ausgabe: Streamlit + Plotly. Stand 2026-10-08. S0 startet in einer neuen Session.

## Ausgangslage

- DB und Dashboard laufen auf **30 erfundenen Tagen** (Fallback in `scripts/ingest_raw_data.py`).
- `.gitignore` ignoriert `models/` und `*.csv`: dbt-Modelle und Seeds sind nicht versioniert. `profiles.yml` ist ignoriert.
- Kern fehlt: Hilfsfrist-Quote pro Region, Karte, Zeitverlauf.
- Repo und `wgnd-toolkit` sind öffentlich (GitHub-API, 2026-10-08). Kein Streamlit- oder Pages-Link im Repo; ob eine Streamlit-App existiert, ist nicht prüfbar.

## Daten (verifiziert, `Berliner-Feuerwehr/BF-Open-Data`, CC BY 4.0)

| Quelle | Granularität | Rolle |
| :--- | :--- | :--- |
| `Mission_Data/*_JJJJ.csv` (2018–2026) | Einsatz, Bezirk (12), Tag, keine Uhrzeit, keine ID | Zeitverlauf |
| `Regional_Data/JJJJ` | 542 Planungsräume, 143 Bezirksregionen, 60 Prognoseräume, nur Jahr, IDs stabil | Karte, Hilfsfrist-Quote |
| `Daily_Data`, `Turnout_Times` (+`current`), `Dispatchcodes` | Stadt/Tag, Wache/Quartal, Code | Trend, Snapshot, Seed |
| LOR-Polygone (Geoportal Berlin) | 542 + 143 Flächen | Karte; Quelle/Lizenz offen |

Upstream hat keinen Tagesendpunkt: täglich wird die Datei des laufenden Jahres neu geladen, Vorjahre einmalig.

## Schritte

| Schritt | Inhalt |
| :--- | :--- |
| **S0 Fundament** | Standard-Dateien aus `wgnd-scaffolding` (Typ `data`, Bestand nachziehen, nichts überschreiben): CLAUDE, ROADMAP, BACKLOG, PROCESS_LOG, Makefile, `public/`-Skeleton; `.gitignore` korrigieren, `profiles.yml` committen, `wgnd` per Git-URL einbinden, README neu, CONCEPT erweitern, `PROJECTS.md` |
| **S1 Ingestion** | `scripts/ingest.py` ersetzt Fake-Skript: `--full` und Daily-Modus, idempotent, harter Fehler statt Fallback, Spaltenprüfung, Fixture |
| **S2 dbt-Kern** | Sources + Freshness, Seeds, Staging, Macros, Intermediate, Marts (incremental), Tests |
| **S3 Geodaten + App** | LOR-Polygone, Parquet-Export, Streamlit auf Parquet, Choropleth mit Jahres-Slider, KPI-Zeile, Event-Marker, Plotly-Theme aus `wgnd`-Palette; `/project-case check` als Zwischenprüfung |
| **S3b Fragestellung + Notebooks** | Notebooks sind die Basisarbeit, die App zeigt nur das Ergebnis. `00_introduction` (Fragestellung, Quellen, dbt-Architektur), `01_exploration_<quelle>` je Quelle mit `wgnd.inspect` + Fazit, `02_preparation` (Pipeline im Detail, Medallion), `03_analysis_<dimension>` (Zeit, Geo, Einsatzart, Sonderereignisse), `04_insights` (belegte Aussagen, Empfehlungen, neue Charts) → `app_data/insights.json` → App-Seite "Befunde". Danach Anreicherung Stufe 1 (Feiertage/Ferien, Wetter) mit Ingestion, dbt-Source und Notebooks `01_exploration_weather`/`_holidays`, `03_analysis_weather`. `make notebooks` führt alle aus |
| **S4 Automatisierung** | `daily.yml` (Cron, Cache, Freshness, Build, Export, Bot-Commit), `pr.yml`, Persistenz der Snapshot-Historie |
| **S5 dbt-Vollständigkeit + Governance** | Snapshots, Docs, Exposures, Selectors, Contracts, Access/Groups, Versions, Meta, Qualitätsbericht |
| **S6 Konsistenz + Case** | Notebook-Konsistenz nach `CONVENTIONS.md`; `/project-review` (nach S5), `/project-case` story → slides; `public/`-Hub mit Link zur Live-App; Streamlit-Deployment-Link |

## Komponente → Schritt

| Komponente | Umsetzung | Schritt |
| :--- | :--- | :--- |
| Sources, Freshness | alle Rohtabellen, `loaded_at_field: _loaded_at` | S2, S4 |
| Seeds | `seed_districts`, `seed_events`, `seed_dispatch_codes` | S2 |
| Staging / Intermediate / Marts | view → view → table/incremental | S2 |
| Incremental | `fct_missions_daily_district`, `delete+insert` auf `mission_date` | S2 |
| Macros, Jinja, Vars | Hilfsfrist-Schwelle, Flag, `safe_pct` | S2 |
| Generic + Singular Tests | `dbt_utils`, eigener Test, Abgleich Bezirksregionen vs. Mission_Data | S2 |
| Snapshots (SCD2) | `snap_regional_current_year`, `snap_turnout_current` | S5 |
| Docs, `doc()`-Blocks, Lineage | Hilfsfrist-Definition, LOR-Hierarchie | S5 |
| Exposures | Streamlit-Dashboard | S5 |
| Selectors, Tags, State | `daily`/`static`, `selectors.yml` | S5, S4 |
| **Contracts** | `contract: enforced` auf den Marts | S5 |
| **Access + Groups** | `public`/`private`, Groups mit Owner | S5 |
| **Model Versions** | eine Version an einem Mart (Übungsteil) | S5 |
| **Meta-Tags** | Owner, Quelle, Lizenz CC BY 4.0 | S5 |
| **Qualitätsbericht** | Testabdeckung je Schicht, bekannte Datenlücken | S5 |
| CI / Orchestrierung | GitHub Actions, täglich + PR | S4 |
| Serving | Streamlit + Plotly | S3 |
| `wgnd`-Toolkit | Git-URL-Dependency; Plotly-Theme als neues, versioniertes Toolkit-Feature; Notebooks | S0, S3, S6 |
| Portfolio-Skills | Init-Standard, `check` nach S3, `review` nach S5, `story`/`slides` | S0, S3, S5, S6 |

## Qualitäts- und Governance-Details (S5)

- Contracts: Spaltennamen, Typen, `not_null`/Constraints auf allen Marts.
- Groups: ein Owner (Kay), Marts `public`, Staging/Intermediate `private`.
- Version: `fct_timegoal_region_yearly` v1 → v2 (z. B. zusätzliche Spalte), `latest_version` und Deprecation dokumentiert.
- Qualitätsbericht (Markdown, aus `run_results.json` erzeugt): Tests je Schicht, Datenlücken (Telefonie-Ausfall 2024/25, leere `response_time`, Korrekturen in Vorjahren).

## Anreicherung

- **Stufe 1 (S3b):** Feiertage/Ferien, Wetter (Open-Meteo, täglich, Berlin).
- **Stufe 2 (später):** Einwohner je Planungsraum, Wachen-Koordinaten, Turnout-Vergleich, KV-/Call-Data.
- Politik nur als belegte Annotation (`seed_events`), keine Kausalaussage.

## Offene Verifikationen (im jeweiligen Schritt)

- Bedeutung von `dispatchcode_criticality` (A/C/D/E) und Stufe „kritisch" (Vermutung: Dringlichkeitsstufe, nicht Führungsdienst).
- Hilfsfrist-Schwelle (Vermutung 600 s) gegen Regional-Quote.
- URL und Lizenz der LOR-Polygone, Dateigröße nach Vereinfachung.
- Duplikate ohne Einsatz-ID, nachträgliche Korrekturen in Vorjahresdateien.

## Verifikation (Ende-zu-Ende)
- `ingest.py --full` lädt Daten bis gestern, bricht bei kaputter URL ab, erzeugt keine Duplikate; `dbt build` + Freshness grün, manipulierter Wert lässt Abgleich-Test rot werden.
- Karte zeigt 143/542 Flächen ohne Lücken; `workflow_dispatch` testet Cache, Bot-Commit, Redeploy.
