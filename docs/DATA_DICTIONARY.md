# Data Dictionary – Berlin Emergency Response

Dieses Dokument beschreibt die Quelltabellen (Sources) und die daraus abgeleiteten Staging-Modelle im Data Warehouse.

---

## 1. Raw Layer (`raw_fire_department`)

### `raw_missions_daily`
Unveränderte Rohdaten der täglichen Einsatzzahlen der Berliner Feuerwehr.

| Spalte | Datentyp | Beschreibung | Beispiel |
| :--- | :--- | :--- | :--- |
| `datum` | VARCHAR / DATE | Datum des Einsatztages (Format `YYYY-MM-DD`) | `2026-01-15` |
| `einsaetze_gesamt` | BIGINT | Gesamtzahl aller dispositionierten Einsätze an diesem Tag | `420` |
| `rettungsdienst_einsaetze` | BIGINT | Anzahl der medizinischen Rettungseinsätze (RTW/NEF) | `350` |
| `feuerwehr_einsaetze` | BIGINT | Anzahl der Brandeinsätze und technischen Hilfeleistungen | `70` |
| `antwortzeit_mediana` | DOUBLE | Median der Antwortzeit/Dispositionszeit in Sekunden | `495.2` |
| `_loaded_at` | TIMESTAMP | Technischer Zeitstempel der Ingestion in DuckDB | `2026-10-05 14:00:00` |

---

## 2. Staging Layer (`staging`)

### `stg_missions_daily`
Bereinigtes, typisiertes und auf Englisch standardisiertes Staging-Modell.

| Spalte | Datentyp | Primärschlüssel / Tests | Beschreibung |
| :--- | :--- | :--- | :--- |
| `mission_date` | DATE | PK (`unique`, `not_null`) | Datum des Einsatztages |
| `total_missions` | INTEGER | `>= 0` | Gesamtzahl der Einsätze |
| `rescue_missions` | INTEGER | `>= 0` | Anzahl Rettungsdienst-Einsätze |
| `fire_missions` | INTEGER | `>= 0` | Anzahl Feuerwehr-Einsätze |
| `median_response_time_seconds` | DOUBLE | NULL oder `> 0` | Median der Antwortzeit in Sekunden |
| `loaded_at` | TIMESTAMP | `not_null` | Ingestion-Zeitstempel für Auditing / Freshness |