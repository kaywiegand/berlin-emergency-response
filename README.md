# Berlin Emergency Response — dbt Certification Edition

> Vorbereitungsprojekt auf die **dbt Analytics Engineering Certification** anhand der Open Data der Berliner Feuerwehr.
> Das Projekt verbindet dbt-Best-Practices mit modernem AI-supported Engineering und einer schlanken Cloud-Pipeline.

---

## 🚀 Ziel & Zweck des Projekts

Dieses Repository dient als zentrales Praxisfeld für die **dbt Analytics Engineering Certification**. Das Ziel ist es, den gesamten Lebenszyklus eines modernen Data-Engineering- und Analytics-Projekts abzubilden — von der Rohdaten-Infrastruktur bis zur BI-Bereitstellung.

### Was dieses Repository abdeckt (über `CONCEPT.md` und `DATA_SOURCES.md` hinaus):

1. **Vollständige Prüfungsvorbereitung**
   - Direkte Umsetzung aller 7 Domain-Schwerpunkte der dbt Certification (Seeds, Snapshots, Incremental Models, Testing, Jinja/Macros, Exposures, CLI-Tuning).
2. **AI-Assisted Workflow & Tooling Integration**
   - Nutzung von **Claude Code / Custom Skills** für automatisierte Reviews, Dokumentationserstellung und CI-Standardisierung.
   - Praxisnahes Testing von Agentic Data Engineering Workflows.
3. **End-to-End Modern Data Stack (Local & CI)**
   - Vollständige Entkopplung von teuren Data Warehouses durch die Kombination aus **DuckDB + dbt-core**.
   - Automatisierte Ausführung & Schema-Validierung bei jedem PR via GitHub Actions.

---

## 🛠 Tech Stack & Komponenten

| Schicht | Technologie | Aufgabe im Projekt |
| :--- | :--- | :--- |
| **Ingestion** | Python (`httpx`, `pandas`) | Gezieltes Herunterladen der Tages- und Einsatzdaten (ohne 6.8 GB Repo-Clone) |
| **Storage / Engine** | DuckDB | Embedded OLAP Data Warehouse |
| **Transformation** | dbt-core (`dbt-duckdb`) | Modularisierung (Staging, Intermediate, Marts), Testing & Macros |
| **Quality & Tests** | dbt-tests + `dbt-utils` | Generic & Custom Singular SQL Tests zur Datenqualität |
| **BI / Serving** | Evidence.dev | Code-based / SQL-native Data App (exportiert als statisches HTML) |
| **Orchestrierung & CI** | GitHub Actions | Tägliche Ingestion-Runs und automatisierte PR-Builds (`dbt build`) |
| **Hosting** | GitHub Pages | Kostenlose Bereitstellung des Evidence.dev Dashboards |

---

## 📂 Projektstruktur & Geplante Bestandteile

```
.
├── .github/workflows/      # CI/CD Pipelines (z. B. automated dbt build & test)
├── data/                   # DuckDB Datenbankdatei (`berlin_emergency.duckdb`)
├── docs/                   # Projektdokumentation & Konzepte
│   ├── CONCEPT.md          # Fachliches Konzept & Zertifizierungs-Matrix
│   └── DATA_SOURCES.md     # Evaluierung der Feuerwehr-Open-Data Endpunkte
├── macros/                 # Custom Jinja UDFs (z. B. Hilfsfrist-Berechnung)
├── models/
│   ├── staging/            # Staging Models, Renaming, Typisierung, sources.yml
│   ├── intermediate/       # Fachliche Aggregationen & Logik-Verknüpfungen
│   └── marts/              # Dimensionen & Incremental Fact Tables (z. B. fct_missions_daily)
├── scripts/                # Python-Skripte für Ingestion & Maintenance (`ingest_raw_data.py`)
├── seeds/                  # CSV-Mappings (z. B. Zuordnung Bezirksregionen → Bezirke)
├── snapshots/              # Type-2 SCDs (z. B. Wachen-Status & Fahrzeugkapazitäten)
├── tests/                  # Custom Singular SQL Quality Tests
├── .gitignore              # Git-Ignore (u. a. `.venv/`, `data/`, `profiles.yml`)
├── .python-version         # Geplante Python-Version für uv
├── dbt_project.yml         # dbt Projekt-Konfiguration
├── package-lock.yml        # Generierter Lock-State von dbt-Packages
├── packages.yml            # dbt External Packages (z. B. `dbt_utils`)
├── profiles.yml            # dbt Connection Credentials für DuckDB
├── pyproject.toml          # Python-Projektkonfiguration & Dependencies (uv)
├── uv.lock                 # Exakter Deterministic Package Lock-State für Python
└── README.md               # Projekt-Überblick & Setup-Anleitung
```



Hier ist die aktualisierte und vollständige Projektstruktur für deine **`README.md`**.

Sie berücksichtigt das aktuelle `uv`-Environment Setup (`pyproject.toml`, `uv.lock`), die Verortung der Dokumentation in `docs/` sowie die Ordner für Skripte, dbt-Packages und DuckDB-Datenbanken:

```markdown
## 📂 Projektstruktur

```text
.
├── .github/workflows/      # CI/CD Pipelines (z. B. automated dbt build & test)
├── data/                   # DuckDB Datenbankdatei (`berlin_emergency.duckdb`)
├── docs/                   # Projektdokumentation & Konzepte
│   ├── CONCEPT.md          # Fachliches Konzept & Zertifizierungs-Matrix
│   ├── DATA_DICTIONARY.md  # Datenwörterbuch (Sources & Models)
│   └── DATA_SOURCES.md     # Evaluierung der Feuerwehr-Open-Data Endpunkte
├── macros/                 # Custom Jinja UDFs (z. B. Hilfsfrist-Berechnung)
├── models/
│   ├── staging/            # Staging Models, Renaming, Typisierung, sources.yml
│   ├── intermediate/       # Fachliche Aggregationen & Logik-Verknüpfungen
│   └── marts/              # Dimensionen & Incremental Fact Tables (z. B. fct_missions_daily)
├── scripts/                # Python-Skripte für Ingestion & Maintenance (`ingest_raw_data.py`)
├── seeds/                  # CSV-Mappings (z. B. Zuordnung Bezirksregionen → Bezirke)
├── snapshots/              # Type-2 SCDs (z. B. Wachen-Status & Fahrzeugkapazitäten)
├── tests/                  # Custom Singular SQL Quality Tests
├── .gitignore              # Git-Ignore (u. a. `.venv/`, `data/`, `profiles.yml`)
├── .python-version         # Geplante Python-Version für uv
├── dbt_project.yml         # dbt Projekt-Konfiguration
├── package-lock.yml        # Generierter Lock-State von dbt-Packages
├── packages.yml            # dbt External Packages (z. B. `dbt_utils`)
├── profiles.yml            # dbt Connection Credentials für DuckDB
├── pyproject.toml          # Python-Projektkonfiguration & Dependencies (uv)
├── uv.lock                 # Exakter Deterministic Package Lock-State für Python
└── README.md               # Projekt-Überblick & Setup-Anleitung

```

---

### Nächste Schritte:

1. Ingestion ausführen: `uv run python scripts/ingest_raw_data.py`
2. Staging-Model bauen: `uv run dbt run`
3. Tests durchführen: `uv run dbt testHier ist die aktualisierte und vollständige Projektstruktur für deine **`README.md`**.

Sie berücksichtigt das aktuelle `uv`-Environment Setup (`pyproject.toml`, `uv.lock`), die Verortung der Dokumentation in `docs/` sowie die Ordner für Skripte, dbt-Packages und DuckDB-Datenbanken:

```markdown
## 📂 Projektstruktur

```text
.
├── .github/workflows/      # CI/CD Pipelines (z. B. automated dbt build & test)
├── data/                   # DuckDB Datenbankdatei (`berlin_emergency.duckdb`)
├── docs/                   # Projektdokumentation & Konzepte
│   ├── CONCEPT.md          # Fachliches Konzept & Zertifizierungs-Matrix
│   └── DATA_SOURCES.md     # Evaluierung der Feuerwehr-Open-Data Endpunkte
├── macros/                 # Custom Jinja UDFs (z. B. Hilfsfrist-Berechnung)
├── models/
│   ├── staging/            # Staging Models, Renaming, Typisierung, sources.yml
│   ├── intermediate/       # Fachliche Aggregationen & Logik-Verknüpfungen
│   └── marts/              # Dimensionen & Incremental Fact Tables (z. B. fct_missions_daily
├── src/
│   ├── utils/
│   │   ├── __init__.py      # Macht den Ordner zu einem Python-Package
│   │   └── plots.py         # Unsere Plotly-Funktionen
│   └── app.py               # Das Streamlit-Dashboard
├── notebooks/
│   └── explore_dashboard.ipynb
├── scripts/                # Python-Skripte für Ingestion & Maintenance (`ingest_raw_data.py`)
├── seeds/                  # CSV-Mappings (z. B. Zuordnung Bezirksregionen → Bezirke)
├── snapshots/              # Type-2 SCDs (z. B. Wachen-Status & Fahrzeugkapazitäten)
├── tests/                  # Custom Singular SQL Quality Tests
├── .gitignore              # Git-Ignore (u. a. `.venv/`, `data/`, `profiles.yml`)
├── .python-version         # Geplante Python-Version für uv
├── dbt_project.yml         # dbt Projekt-Konfiguration
├── package-lock.yml        # Generierter Lock-State von dbt-Packages
├── packages.yml            # dbt External Packages (z. B. `dbt_utils`)
├── profiles.yml            # dbt Connection Credentials für DuckDB
├── pyproject.toml          # Python-Projektkonfiguration & Dependencies (uv)
├── uv.lock                 # Exakter Deterministic Package Lock-State für Python
└── README.md               # Projekt-Überblick & Setup-Anleitung

```


### Nächste Schritte:

1. Ingestion ausführen: `uv run python scripts/ingest_raw_data.py`
2. Staging-Model bauen: `uv run dbt run`
3. Tests durchführen: `uv run dbt test`

```


### Testing & Data Quality Strategy
In a robust analytics engineering workflow, testing is not an afterthought—it is a core architectural requirement. To ensure our data products are reliable, trustworthy, and ready for production use, we implement a comprehensive testing strategy across the entire pipeline.
1. Warum testen wir? (The "Why")
Data pipelines are vulnerable to silent failures: upstream schema changes, unexpected null values, duplicate records, or calculation errors in business logic. Without automated testing, these errors propagate straight into dashboards and executive reports. Automated data testing ensures:
Early Detection: Catching anomalies at ingestion or transformation time rather than in production dashboards.
Trust & Reliability: Establishing a guaranteed "Single Source of Truth."
CI/CD Safety: Allowing safe refactoring and continuous integration without fear of breaking downstream dependencies.
2. Wo testen wir? (The "Where" – The Sandwich Pattern)
Rather than testing randomly, we employ a two-layer "Sandwich" Testing Architecture:
Staging Layer (stg_): Focuses on technical data integrity. We validate that raw inputs conform to expected formats, primary keys (mission_date) are unique, and mandatory fields are not null.
Marts Layer (fct_): Focuses on business logic and analytical correctness. Here we validate final aggregations, rolling averages, and metric constraints before data is exposed to BI tools or applications.
3. Wie testen wir? (The "How")
Testing is declaratively embedded directly into the dbt workflow using YAML configurations (schema.yml) combined with automated SQL test generation:
Singular Tests: Built-in generic assertions (unique, not_null) executed natively against the data warehouse.
Execution & Automation: Tests are executed via CLI (dbt test) and integrated into automated pipeline runs to block faulty deployments.