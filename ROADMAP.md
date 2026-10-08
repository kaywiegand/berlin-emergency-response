# ROADMAP.md — Berlin Emergency Response

> Konzeptionell. Details je Schritt in `docs/PLAN.md`.

**Ausgangslage:** Pipeline und Dashboard laufen auf 30 erfundenen Tagen. Kern fehlt: Hilfsfrist-Quote pro Region, Karte, Zeitverlauf.
**Ziel:** Echte BF-Open-Data täglich aktuell, vollständige dbt-Abdeckung, Streamlit-Dashboard mit Karte, Portfolio-Case.

## Phasen

- [ ] **S0 Fundament** — Repo-Hygiene, Standard-Dateien, `wgnd`
- [ ] **S1 Ingestion** — `scripts/ingest.py`, idempotent, kein Fallback
- [ ] **S2 dbt-Kern** — Sources, Seeds, Staging, Macros, Intermediate, Marts, Tests
- [ ] **S3 Geodaten + App** — LOR-Polygone, Parquet, Choropleth, Plotly-Theme
- [ ] **S4 Automatisierung** — GitHub Actions täglich + PR
- [ ] **S5 dbt-Vollständigkeit + Governance** — Snapshots, Docs, Contracts, Groups, Versions, Qualitätsbericht
- [ ] **S6 Konsistenz + Case** — Notebooks, `/project-review`, `/project-case`
