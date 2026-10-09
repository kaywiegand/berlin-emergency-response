# Berlin Emergency Response

Wie schnell ist der Berliner Rettungsdienst bei kritischen Notfällen vor Ort, in welchen Regionen wird die Hilfsfrist verfehlt, und wie verschiebt sich das über die Jahre?

Das Projekt baut dafür eine vollständige Analytics-Engineering-Pipeline auf den Open Data der Berliner Feuerwehr: Ingestion, dbt-Transformation auf DuckDB, Streamlit-Dashboard mit Karte, tägliche Automatisierung über GitHub Actions. Es dient zugleich als Portfolio-Case und als Praxisprojekt zur dbt Analytics Engineering Certification.

**Abgrenzung:** keine Bewertung von Einsatzkräften. Antwortzeiten hängen an Standortdichte, Verkehr, Bebauung und Einsatzaufkommen. Das Projekt beschreibt Struktur, nicht Verschulden.

**Status:** im Aufbau. Aktueller Stand in [`PROCESS_LOG.md`](PROCESS_LOG.md), Vorhaben in [`docs/PLAN.md`](docs/PLAN.md).

---

## Architektur

```
BF-Open-Data (GitHub, CC BY 4.0)
   │  gezielter Abruf einzelner Dateien (kein Clone)
   ▼
Ingestion (Python)  ──►  DuckDB (raw)
                            │
                            ▼
                    dbt: staging → intermediate → marts
                            │
                            ▼
                  Parquet-Export  ──►  Streamlit + Plotly
```

| Schicht | Werkzeug |
| :--- | :--- |
| Ingestion | Python (`httpx`, `pandas`) |
| Warehouse | DuckDB |
| Transformation, Tests, Docs | dbt-core (`dbt-duckdb`, `dbt_utils`) |
| Serving | Streamlit, Plotly |
| Orchestrierung, CI | GitHub Actions |
| Hilfsbibliothek | [`wgnd`](https://github.com/kaywiegand/wgnd-toolkit) |

Fachliches Konzept: [`docs/CONCEPT.md`](docs/CONCEPT.md) · Quellen: [`docs/DATA_SOURCES.md`](docs/DATA_SOURCES.md) · Datenwörterbuch: [`docs/DATA_DICTIONARY.md`](docs/DATA_DICTIONARY.md)

---

## Setup

Voraussetzung: [`uv`](https://docs.astral.sh/uv/).

```bash
make setup        # uv sync + dbt deps
make dbt-build    # Seeds, Modelle, Tests
make export       # Marts nach app_data/ exportieren
make app          # Streamlit-Dashboard
```

`make help` listet alle Targets.

---

## Projektstruktur

```
.
├── data/            # DuckDB-Datei und Rohdaten (nicht versioniert)
├── docs/            # Plan, Konzept, Quellen, Datenwörterbuch
├── models/          # dbt: staging, intermediate, marts
├── macros/ seeds/ snapshots/ tests/   # dbt
├── scripts/         # Ingestion, LOR-Polygone, Parquet-Export
├── app_data/        # Export für die App (Parquet, GeoJSON)
├── src/             # Streamlit-App (app.py, utils/) und Projektpaket berlin_emergency_response
├── notebooks/       # Exploration und Analyse
├── public/          # Web-Root für GitHub Pages
├── dbt_project.yml · profiles.yml · packages.yml
└── pyproject.toml · uv.lock
```

`profiles.yml` ist versioniert: es enthält nur den lokalen DuckDB-Pfad, keine Zugangsdaten.

---

## Datenqualität

Tests liegen deklarativ in den `schema.yml` der dbt-Schichten (`unique`, `not_null`, `relationships`, `dbt_utils`) plus Singular Tests für fachliche Unmöglichkeiten. `dbt source freshness` prüft, ob Upstream-Daten pünktlich vorliegen.

---

## Lizenz und Datenquelle

Einsatzdaten: Berliner Feuerwehr, [BF-Open-Data](https://github.com/Berliner-Feuerwehr/BF-Open-Data), CC BY 4.0.
Flächen: Amt für Statistik Berlin-Brandenburg / Statistische Einheiten im INSPIRE-Datenmodell (Lebensweltlich Orientierte Räume 01.01.2021), CC BY 3.0 DE.
