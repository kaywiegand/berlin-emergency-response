# ROADMAP.md — Berlin Emergency Response

> Konzeptionell. Details je Schritt in `docs/PLAN.md`.

**Ausgangslage:** Pipeline und Dashboard laufen auf 30 erfundenen Tagen. Kern fehlt: Hilfsfrist-Quote pro Region, Karte, Zeitverlauf.
**Ziel:** Echte BF-Open-Data täglich aktuell, vollständige dbt-Abdeckung, Streamlit-Dashboard mit Karte, Portfolio-Case.

## Phasen

- [x] **S0 Fundament** — Repo-Hygiene, Standard-Dateien, `wgnd`
- [x] **S1 Ingestion** — `scripts/ingest.py`, idempotent, kein Fallback
- [x] **S2 dbt-Kern** — Sources, Seeds, Staging, Macros, Intermediate, Marts, Tests
- [x] **S3 Geodaten + App** — LOR-Polygone, Parquet, Choropleth, Plotly-Theme
- [ ] **S3b Fragestellung + Notebooks** — `00`–`04`, danach Anreicherung Wetter/Feiertage, `insights.json`
- [ ] **S4 Automatisierung** — GitHub Actions täglich + PR
- [ ] **S5 dbt-Vollständigkeit + Governance** — Snapshots, Docs, Contracts, Groups, Versions, Qualitätsbericht
- [ ] **S6 Konsistenz + Case** — Notebooks, `/project-review`, `/project-case`
