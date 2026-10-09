# BACKLOG.md — Berlin Emergency Response

Projektspezifische offene Tasks. Nicht mitten in einer Session den Kontext wechseln — hier notieren.

Prio: `1` = hoch · `2` = mittel · `3` = niedrig

| # | Beschreibung | Prio | Entdeckt in |
| :--- | :--- | :--- | :--- |
| 1 | "Kritisch": Stichtag 25.03.2025 und RD1/RD2 sind belegt (BF Open-Data-Seite, eigene Daten). Offen: wie die BF "kritisch" vor dem Stichtag aus den Dispatchcodes berechnet hat (genaue Regel) — bei BF nachfragen | 2 | S2 |
| 2 | Schwelle 600 s weiter Vermutung: konsistent mit Median/Quote 2025, aber nicht über alle Jahre reproduzierbar | 2 | S2 |
| 4 | Duplikate ohne Einsatz-ID und nachträgliche Korrekturen in Vorjahresdateien prüfen | 2 | PLAN (S1/S2) |
| 5 | `docs/CONCEPT.md`: Abschnitte 3–6 (Serving Evidence.dev → Streamlit, `[cite: n]`-Artefakte) an Abschnitt 7 angleichen | 1 | "Kritisch": Stichtag 25.03.2025 und RD1/RD2 sind belegt (BF Open-Data-Seite, eigene Daten). Offen: wie die BF "kritisch" vor dem Stichtag aus den Dispatchcodes berechnet hat (genaue Regel) — bei BF nachfragen | 2 | S2 |
| 7 | Scaffolding: `DE` als CLI-Choice (→ `wgnd-scaffolding/BACKLOG.md`) | 3 | S0 |
| 8 | `ingest.py` bricht am Jahreswechsel hart ab, falls die Datei des neuen Jahres noch fehlt (404) — Verhalten für `daily.yml` festlegen | 2 | S1 |
| 10 | Daily_Data: Lücken in der Zeitreihe (sieben Tage 2026) per dbt-Test erkennen und im Qualitätsbericht (S5) dokumentieren | 3 | S2 |
| 11 | `seed_dispatch_codes`: ein großer Teil der Codes ohne Namen; Mapping aus `Dispatchcodes/*.xlsx` prüfen | 3 | S2 |
| 12 | Neuer Einsatztyp `Pandemie` (nur in Teilen der Jahre) — Zuordnung zu `mission_group` (derzeit `other`) bewerten | 3 | S2 |
| 14 | 4 Planungsräume heißen bei BF anders als in den LOR (z. B. IDs 12500926/12500930 vertauscht); Karte nutzt den Namen aus dem Parquet (BF) | 3 | S3 |
| 15 | Streamlit-Deployment (Community Cloud o. ä.) und Live-Link für `public/`-Hub — Redeploy-Test in S4, Link in S6 | 2 | S3 |
| 16 | Zeitverlauf-Näherung sinkt 2018 bis 2023 deutlich; Ursache (Dispatch-Code-Zuordnung, Mix der Stufen) in `03_analysis_time` klären, bevor das als Befund gilt | 1 | "Kritisch": Stichtag 25.03.2025 und RD1/RD2 sind belegt (BF Open-Data-Seite, eigene Daten). Offen: wie die BF "kritisch" vor dem Stichtag aus den Dispatchcodes berechnet hat (genaue Regel) — bei BF nachfragen | 2 | S2 |
| 18 | `units_first_type`: Wert `RTW` mit Backtick (Tippfehler in der Quelle) in Staging oder Seed bereinigen (→ `02_preparation`) | 2 | S3b |
| 19 | Regionaldatei 2025 ist etwas kleiner als Einzeleinsätze und Tagesreihe (anders als 2024/2026) — Ursache offen, ggf. bei BF nachfragen | 3 | S3b |
| 20 | Kleine Regionen kennzeichnen (`is_reliable`, Schwelle als dbt-Var) in Mart und Karte | 2 | S3b |
| 21 | `is_partial` für angebrochene Quartale in `stg_turnout_times`/Mart; `dim_station` (LOR-Bezirk und Planungsraum per Punkt in Polygon, `has_rtw_turnout`) auf `seed_stations` | 2 | S3b |
| 22 | `seed_stations` hat Stand 2024: zwei Wachen seit 2026 und eine 2023 aufgegebene fehlen; bei BF nach neuerer Fassung fragen oder belegen | 3 | S3b |
| 23 | Phase-2-Quellen laut Kay: Kiez Data/regionale Kennzahlen (Datensatz klären), DWD Open Data (Wetter), Berlin Open Data (Bevölkerung, Stadtstruktur, weitere Geodaten) — Details in `docs/PLAN.md` | 2 | S3b |
| 24 | Grundsatz "Gesamt immer nach Einsatzart aufgeschlüsselt": umgesetzt in dbt-Schwelle, App, `01_exploration_*` und `04_insights`; ausstehend in `02_preparation` und `03_analysis_*` (beim Schreiben beachten); für technische Hilfe Frist bei BF erfragen oder als nicht vereinbart bestätigen | 1 | S3b |
| 26 | Einsatzcode-Tabelle ist als Seed da (`seed_dispatch_codes`, `seed_dispatch_code_map`); offen: Mapping nur als Prior je Kategorie und Stufe nutzbar (Einzeleinsätze tragen nur 3 von 5 Zeichen), Tabelle ändert sich (Stand 21.05.2026) — Versionierung/Aktualisierung klären | 2 | S3b |
| 29 | Technische Hilfe: Tagesreihe und Einzeleinsätze ergeben rund 13 bis 15 Minuten, die BF-Seite "in Zahlen" nennt 9,92 min als durchschnittlich erreichte Hilfsfrist — Definition klären (Teilmenge? andere Zeit?), bis dahin als offene Abweichung ausweisen | 2 | S3b |
| 30 | `01_exploration_geo`/`_stations` rechnen Abstände mit eigenem Code; auf `berlin_emergency_response.spatial` umstellen (Reuse, wie `04_insights`) | 3 | S3b |
