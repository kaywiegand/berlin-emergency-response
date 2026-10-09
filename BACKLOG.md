# BACKLOG.md — Berlin Emergency Response

Projektspezifische offene Tasks. Nicht mitten in einer Session den Kontext wechseln — hier notieren.

Prio: `1` = hoch · `2` = mittel · `3` = niedrig

| # | Beschreibung | Prio | Entdeckt in |
| :--- | :--- | :--- | :--- |
| 1 | "Kritisch" (Regional `ems_critical`) ist nicht aus `dispatchcode_criticality` nachbaubar (Stufen A–E, O); Definition bei BF erfragen oder Stufe D/E als Näherung dokumentieren. Bruch 2024→2025 in `seed_events` | 1 | S2 |
| 2 | Schwelle 600 s weiter Vermutung: konsistent mit Median/Quote 2025, aber nicht über alle Jahre reproduzierbar | 2 | S2 |
| 4 | Duplikate ohne Einsatz-ID und nachträgliche Korrekturen in Vorjahresdateien prüfen | 2 | PLAN (S1/S2) |
| 5 | `docs/CONCEPT.md`: Abschnitte 3–6 (Serving Evidence.dev → Streamlit, `[cite: n]`-Artefakte) an Abschnitt 7 angleichen | 1 | S0 |
| 6 | `scripts/check_files.py` hängt an entfernten Modellen — löschen | 2 | S1/S3 |
| 7 | Scaffolding: `DE` als CLI-Choice (→ `wgnd-scaffolding/BACKLOG.md`) | 3 | S0 |
| 8 | `ingest.py` bricht am Jahreswechsel hart ab, falls die Datei des neuen Jahres noch fehlt (404) — Verhalten für `daily.yml` festlegen | 2 | S1 |
| 10 | Daily_Data: Lücken in der Zeitreihe (sieben Tage 2026) per dbt-Test erkennen und im Qualitätsbericht (S5) dokumentieren | 3 | S2 |
| 11 | `seed_dispatch_codes`: ein großer Teil der Codes ohne Namen; Mapping aus `Dispatchcodes/*.xlsx` prüfen | 3 | S2 |
| 12 | Neuer Einsatztyp `Pandemie` (nur in Teilen der Jahre) — Zuordnung zu `mission_group` (derzeit `other`) bewerten | 3 | S2 |
| 14 | 4 Planungsräume heißen bei BF anders als in den LOR (z. B. IDs 12500926/12500930 vertauscht); Karte nutzt den Namen aus dem Parquet (BF) | 3 | S3 |
| 15 | Streamlit-Deployment (Community Cloud o. ä.) und Live-Link für `public/`-Hub — Redeploy-Test in S4, Link in S6 | 2 | S3 |
| 16 | Zeitverlauf-Näherung sinkt 2018 bis 2023 deutlich; Ursache (Dispatch-Code-Zuordnung, Mix der Stufen) in `03_analysis_time` klären, bevor das als Befund gilt | 1 | S3 |
| 17 | App: Seite "Befunde" aus `app_data/insights.json` (von `04_insights` erzeugt); App-Texte (Methodik, Hinweise) an die Notebook-Befunde angleichen | 1 | S3b |
| 18 | `units_first_type`: Wert `RTW` mit Backtick (Tippfehler in der Quelle) in Staging oder Seed bereinigen (→ `02_preparation`) | 2 | S3b |
| 19 | Regionaldatei 2025 ist etwas kleiner als Einzeleinsätze und Tagesreihe (anders als 2024/2026) — Ursache offen, ggf. bei BF nachfragen | 3 | S3b |
| 20 | Kleine Regionen kennzeichnen (`is_reliable`, Schwelle als dbt-Var) in Mart und Karte | 2 | S3b |
| 21 | `is_partial` für angebrochene Quartale in `stg_turnout_times`/Mart; `dim_station` (LOR-Bezirk und Planungsraum per Punkt in Polygon, `has_rtw_turnout`) auf `seed_stations` | 2 | S3b |
| 22 | `seed_stations` hat Stand 2024: zwei Wachen seit 2026 und eine 2023 aufgegebene fehlen; bei BF nach neuerer Fassung fragen oder belegen | 3 | S3b |
| 23 | Phase-2-Quellen laut Kay: Kiez Data/regionale Kennzahlen (Datensatz klären), DWD Open Data (Wetter), Berlin Open Data (Bevölkerung, Stadtstruktur, weitere Geodaten) — Details in `docs/PLAN.md` | 2 | S3b |
| 24 | Grundsatz "Gesamt immer nach Einsatzart aufgeschlüsselt" (README, CLAUDE.md) in allen Notebooks, Marts und der App umsetzen; Fristen je Einsatzart; für technische Hilfe Frist bei BF erfragen | 1 | S3b |
| 25 | dbt: `is_within_timegoal` wendet 600 s auf alle `mission_group`-Werte an, sinnvoll nur für Rettungsdienst — Schwelle je Gruppe oder Flag nur für `ems` | 1 | S3b |
| 26 | Dispatch-Codes: BF-Tabelle (`Dispatchcodes/*.xlsx`, Stand 21.05.2026, vollständige AMPDS-Codes mit Notfallkategorie) als Seed nutzen; Mission_Data enthält nur Kategorie und Stufe (3 von 5 Zeichen), eindeutige Zuordnung nur für einen Teil der Kombinationen. RD1+RD2 ist laut Tagesreihe über die Jahre stabil (rund die Hälfte der RD-Einsätze) und die vergleichbare "kritisch"-Gruppe | 1 | S3b |
| 27 | Ergebnis/App: die Diagramme der BF-Open-Data-Seite mindestens nachbauen (Einsatzzahlen nach Art, Anstieg über die Jahre, Eintreffzeiten Notfallrettung, Reanimation, Brand, Notfallkategorien, Prognoseräume) und mit unseren Befunden ergänzen | 1 | S3b |
| 28 | `seed_events` belegen und ergänzen: RTW-B-Einführung (um Jahreswechsel 2022/23), Stürme (Ylenia Feb 2022, Ziros Jun 2025, Klaus 2019) laut BF-Diagrammen; genaue Daten aus Quellen | 2 | S3b |
| 29 | Technische Hilfe: Tagesreihe und Einzeleinsätze ergeben rund 13 bis 15 Minuten, die BF-Seite "in Zahlen" nennt 9,92 min als durchschnittlich erreichte Hilfsfrist — Definition klären (Teilmenge? andere Zeit?), bis dahin als offene Abweichung ausweisen | 2 | S3b |
