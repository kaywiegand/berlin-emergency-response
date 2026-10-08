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
| Seeds | `seed_districts`, `seed_dispatch_codes`, `seed_events` | `seeds/schema.yml` |
| Staging (view) | `stg_missions`, `stg_daily_missions`, `stg_regional_*` (3), `stg_turnout_times` | `models/staging/schema.yml` |
| Intermediate (view) | `int_missions_enriched`, `int_regional_timegoal` | `models/intermediate/schema.yml` |
| Marts | `dim_district`, `dim_region`, `fct_timegoal_region_yearly`, `fct_missions_daily_district` (incremental), `fct_missions_daily_citywide`, `fct_turnout_times_quarterly` | `models/marts/schema.yml` |

## Kennzahlen

| Kennzahl | Quelle | Hinweis |
| :--- | :--- | :--- |
| Hilfsfrist-Quote (offiziell) | `fct_timegoal_region_yearly.ems_critical_timegoal_quote` | 2024–2026. Grundgesamtheit "kritisch" ändert sich 2024→2025 (`seed_events`) |
| Anteil Einsätze ≤ Schwelle (eigene Näherung) | `fct_missions_daily_district.mission_count_within_timegoal` | Schwelle `var timegoal_seconds` (600, Vermutung); je Kritikalitätsstufe, kein binäres "kritisch" |
