# BACKLOG.md — Berlin Emergency Response

Projektspezifische offene Tasks. Nicht mitten in einer Session den Kontext wechseln — hier notieren.

Prio: `1` = hoch · `2` = mittel · `3` = niedrig

| # | Beschreibung | Prio | Entdeckt in |
| :--- | :--- | :--- | :--- |
| 1 | Bedeutung `dispatchcode_criticality` (A/C/D/E) und Stufe "kritisch" klären | 1 | PLAN (S2) |
| 2 | Hilfsfrist-Schwelle (Vermutung 600 s) gegen Regional-Quote verifizieren | 1 | PLAN (S2) |
| 3 | URL und Lizenz der LOR-Polygone klären, Dateigröße nach Vereinfachung | 1 | PLAN (S3) |
| 4 | Duplikate ohne Einsatz-ID und nachträgliche Korrekturen in Vorjahresdateien prüfen | 2 | PLAN (S1/S2) |
| 5 | `docs/CONCEPT.md`: Serving-Schicht Evidence.dev → Streamlit angleichen, `[cite: n]`-Artefakte entfernen | 1 | S0 |
| 6 | `src/app.py`, `scripts/check_files.py` und alte dbt-Modelle hängen an `raw_missions_daily` (erfunden) — in S2/S3 auf neue Raw-Tabellen umstellen, Altlast-Tabelle droppen | 1 | S1 |
| 7 | Scaffolding: `DE` als CLI-Choice (→ `wgnd-scaffolding/BACKLOG.md`) | 3 | S0 |
| 8 | `ingest.py` bricht am Jahreswechsel hart ab, falls die Datei des neuen Jahres noch fehlt (404) — Verhalten für `daily.yml` festlegen | 2 | S1 |
| 9 | Prognoseräume: Regional-Datei 2026 hat 58 Zeilen, PLAN nennt 60 — klären; Regional-Daten gibt es nur ab 2024 (Karten-Slider: 3 Jahre) | 2 | S1 |
