# BACKLOG.md — Berlin Emergency Response

Projektspezifische offene Tasks. Nicht mitten in einer Session den Kontext wechseln — hier notieren.

Prio: `1` = hoch · `2` = mittel · `3` = niedrig

| # | Beschreibung | Prio | Entdeckt in |
| :--- | :--- | :--- | :--- |
| 1 | "Kritisch" (Regional `ems_critical`) ist nicht aus `dispatchcode_criticality` nachbaubar (Stufen A–E, O); Definition bei BF erfragen oder Stufe D/E als Näherung dokumentieren. Bruch 2024→2025 in `seed_events` | 1 | S2 |
| 2 | Schwelle 600 s weiter Vermutung: konsistent mit Median/Quote 2025, aber nicht über alle Jahre reproduzierbar | 2 | S2 |
| 4 | Duplikate ohne Einsatz-ID und nachträgliche Korrekturen in Vorjahresdateien prüfen | 2 | PLAN (S1/S2) |
| 5 | `docs/CONCEPT.md`: Serving-Schicht Evidence.dev → Streamlit angleichen, `[cite: n]`-Artefakte entfernen | 1 | S0 |
| 6 | `scripts/check_files.py` hängt an entfernten Modellen — löschen; Notebooks 01–03 zeigen auf die alte Struktur (S6) | 2 | S1/S3 |
| 7 | Scaffolding: `DE` als CLI-Choice (→ `wgnd-scaffolding/BACKLOG.md`) | 8 | `ingest.py` bricht am Jahreswechsel hart ab, falls die Datei des neuen Jahres noch fehlt (404) — Verhalten für `daily.yml` festlegen | 2 | S1 |
| 9 | Prognoseräume: Regional-Datei 2026 hat 58 Zeilen, PLAN nennt 60 — klären; Regional-Daten gibt es nur ab 2024 (Karten-Slider: 3 Jahre) | 2 | S1 |
| 10 | Daily_Data 2026 liegt ~2 % unter Mission_Data (kein Test dafür) — Ursache klären | 11 | `seed_dispatch_codes`: knapp die Hälfte der Codes ohne Namen; Mapping aus `Dispatchcodes/*.xlsx` prüfen | 12 | Neuer Einsatztyp `Pandemie` (nur in Teilen der Jahre) — Zuordnung zu `mission_group` (derzeit `other`) bewerten | 13 | `wgnd` v0.4.0 (Plotly-Theme) liegt nur lokal (Commit in `wgnd-toolkit`, nicht gepusht) — nach Push `uv lock` hier, dann zeigt die Git-URL auf den neuen Stand; bis dahin lokal editierbar installiert (`uv run --no-sync`) | 1 | S3 |
| 14 | 4 Planungsräume heißen bei BF anders als in den LOR (z. B. IDs 12500926/12500930 vertauscht); Karte nutzt den Namen aus dem Parquet (BF) | 3 | S3 |
| 15 | Streamlit-Deployment (Community Cloud o. ä.) und Live-Link für `public/`-Hub — in S4/S6 | 2 | S3 |
| 16 | Zeitverlauf-Näherung sinkt 2018 bis 2023 deutlich; Ursache (Dispatch-Code-Zuordnung, Mix der Stufen) klären, bevor das als Befund gilt | 1 | S3 |
