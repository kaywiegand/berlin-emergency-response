# Berlin Emergency Response

Welche Faktoren hängen mit der Antwortzeit des Berliner Rettungsdienstes zusammen, und wo und wann wird die Hilfsfrist verfehlt? Die Open Data der Berliner Feuerwehr werden dafür mit weiteren Daten angereichert. Gezeigt werden Zusammenhänge, keine Ursachen.

Die Notebooks (`notebooks/00`–`04`) sind die Analysearbeit, die App zeigt die geprüften Ergebnisse. Dahinter liegt eine vollständige Analytics-Engineering-Pipeline auf den Open Data der Berliner Feuerwehr: Ingestion, dbt-Transformation auf DuckDB, Streamlit-Dashboard mit Karte, tägliche Automatisierung über GitHub Actions. Es dient zugleich als Portfolio-Case und als Praxisprojekt zur dbt Analytics Engineering Certification.

**Abgrenzung:** keine Bewertung von Einsatzkräften. Antwortzeiten hängen an Standortdichte, Verkehr, Bebauung und Einsatzaufkommen. Das Projekt beschreibt Struktur, nicht Verschulden.

**Status:** im Aufbau. Aktueller Stand in [`PROCESS_LOG.md`](PROCESS_LOG.md), Vorhaben in [`docs/PLAN.md`](docs/PLAN.md).

---

## Fristen und Schutzziele

Die Berliner Feuerwehr arbeitet in drei Einsatzarten, für die **unterschiedliche Vorgaben** gelten. Eine einzige "Hilfsfrist" gibt es nicht.

| Einsatzart | Vorgabe (Schutzziel) | Gemessen als |
| :--- | :--- | :--- |
| **Rettungsdienst** | Zwei Einsatzkräfte innerhalb von 10 Minuten (Planungsgröße), Erreichungsgrad 90 % vereinbart | Zeit bis zum Eintreffen des ersten Fahrzeugs |
| **Brandbekämpfung** | 14 Funktionen innerhalb von 15 Minuten; Erreichungsgrad 90 % in Schutzzielklasse A, 50 % in Klasse B | Zeit bis zum ersten wasserführenden Fahrzeug, zur ersten Drehleiter und bis 14 Einsatzkräfte vor Ort sind |
| **Technische Hilfeleistung** | keine Frist gefunden | nur Antwortzeit-Statistik, keine Hilfsfrist-Auswertung der Feuerwehr |

Quellen: [Senatsantwort 2019](https://pardok.parlament-berlin.de/starweb/adis/citat/VT/19/SchrAnfr/S19-19457.pdf), [Jahresbericht 2022](https://www.berliner-feuerwehr.de/fileadmin/bfw/dokumente/Publikationen/Jahresberichte_infografik/Infografik_Jahresbericht_2022_innen.pdf), [Jahresbericht 2023](https://www.berliner-feuerwehr.de/fileadmin/bfw/dokumente/Publikationen/Jahresberichte_infografik/Infografik_Jahresbericht_2023.pdf), [Open-Data-Seite der Feuerwehr](https://www.berliner-feuerwehr.de/service/open-data/). Den Gesetzestext haben wir nicht geprüft.

**Folgen für das Projekt**

- **Gesamtbetrachtungen sind immer nach Einsatzart aufgeschlüsselt.** Eine Zahl über alle Einsätze mischt Vorgaben, die nicht vergleichbar sind. Jede Auswertung zeigt zuerst das Gesamtbild und direkt daneben die Aufteilung in Rettungsdienst, Brandbekämpfung und technische Hilfeleistung, jeweils mit der passenden Frist (oder dem Hinweis, dass es keine gibt).
- **Die Hilfsfrist-Quote ist nur für den Rettungsdienst und die Brandbekämpfung definiert.** Die offizielle Quote in den Regionaldaten gilt nur für *kritische* Rettungsdiensteinsätze und für Brände.
- **"Kritisch" ist kein stabiler Begriff:** Seit dem 25.03.2025 klassifiziert die Feuerwehr Rettungsdiensteinsätze in Notfallkategorien (RD1 bis RD5). Die Zahl "kritischer" Einsätze fällt dadurch sprunghaft; Jahresvergleiche der Quote sind nur mit Vorsicht möglich.
- **Weitere Strukturänderung:** Die Einführung des RTW-B (Basic Life Support) um den Jahreswechsel 2022/23 verschiebt die Hilfsfrist ebenfalls, laut Darstellung der Feuerwehr.

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
Wachen-Standorte: Berliner Feuerwehr, Geoportal Berlin (dl-de-zero-2.0).
Flächen: Amt für Statistik Berlin-Brandenburg / Statistische Einheiten im INSPIRE-Datenmodell (Lebensweltlich Orientierte Räume 01.01.2021), CC BY 3.0 DE.
