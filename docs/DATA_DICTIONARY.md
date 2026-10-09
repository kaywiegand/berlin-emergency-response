# Data Dictionary — Berlin Emergency Response

> Einstieg in die Datenschichten. Spaltenbeschreibungen und Tests stehen in den `schema.yml` der Schichten, die generierte dbt-Doku (`dbt docs`, S5) ist die Referenz.

## Raw (`scripts/ingest.py`)

Alle Spalten `VARCHAR`, dazu `_partition`, `_source_file`, `_loaded_at`. Partition = Jahr, Quartal, `current` oder `all`.

| Tabelle | Quelle | Partition |
| :--- | :--- | :--- |
| `raw_mission_data` | `Mission_Data/*.csv` | Jahr (2018–) |
| `raw_daily_mission_data` | `Daily_Data/BFw_mission_data_daily.csv` | `all` |
| `raw_regional_planning_room` | `Regional_Data/<Jahr>` | Jahr (2024–) |
| `raw_regional_district_area` | `Regional_Data/<Jahr>` | Jahr (2024–) |
| `raw_regional_prediction_area` | `Regional_Data/<Jahr>` | Jahr (2024–) |
| `raw_turnout_times` | `Turnout_Times/*.csv` | Quartal, `current` |

## dbt

| Schicht | Modelle | Quelle der Beschreibung |
| :--- | :--- | :--- |
| Seeds | `seed_districts`, `seed_dispatch_codes`, `seed_events` | `dbt/seeds/schema.yml` |
| Staging (view) | `stg_missions`, `stg_daily_missions`, `stg_regional_*` (3), `stg_turnout_times` | `dbt/models/staging/schema.yml` |
| Intermediate (view) | `int_missions_enriched`, `int_regional_timegoal` | `dbt/models/intermediate/schema.yml` |
| Marts | `dim_district`, `dim_region`, `fct_timegoal_region_yearly`, `fct_missions_daily_district` (incremental), `fct_missions_daily_citywide`, `fct_turnout_times_quarterly` | `dbt/models/marts/schema.yml` |

## Kennzahlen

| Kennzahl | Quelle | Hinweis |
| :--- | :--- | :--- |
| Hilfsfrist-Quote (offiziell) | `fct_timegoal_region_yearly.ems_critical_timegoal_quote` | 2024–2026. Grundgesamtheit "kritisch" ändert sich 2024→2025 (`seed_events`) |
| Anteil Einsätze ≤ Schwelle (eigene Näherung) | `fct_missions_daily_district.mission_count_within_timegoal` | Schwelle `var timegoal_seconds` (600, Vermutung); je Kritikalitätsstufe, kein binäres "kritisch" |

## App-Export (`scripts/export_parquet.py`, `scripts/fetch_lor.py`)

| Datei | Inhalt |
| :--- | :--- |
| `public/app/data/timegoal_region_yearly.parquet` | offizielle Hilfsfrist-Zahlen je LOR-Region und Jahr (mit Bezirk) |
| `public/app/data/missions_monthly.parquet` | Monat × Bezirk × Gruppe × Stufe, additive Zähler und Summe der Antwortzeit |
| `public/app/data/missions_daily_citywide.parquet` | Stadt/Tag aus Daily_Data |
| `public/app/data/turnout_quarterly.parquet` | Ausrückzeiten je Wache und Quartal |
| `public/app/data/events.parquet`, `districts.parquet` | Seeds für Event-Marker und Bezirke |
| `public/app/data/geo/lor_<ebene>.geojson` | vereinfachte LOR-Polygone (EPSG:4326), 3 Ebenen |
| `public/app/data/geo/fire_operational_areas.geojson` | sechs Einsatzbereiche der Feuerwehr (Geoportal Berlin) |
| `dbt/seeds/seed_stations.csv` | 102 Feuerwehr-Standorte mit Koordinaten, Typ, Bezirk, Einsatzbereich (Geoportal Berlin, Stand 2024) |
| `public/app/data/meta.json` | Datenstand und Exportzeitpunkt |
