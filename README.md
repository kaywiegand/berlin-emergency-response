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
| **Technische Hilfeleistung** | keine Frist und kein Erreichungsgrad vereinbart; die Feuerwehr weist nur die durchschnittlich erreichte Hilfsfrist aus | Antwortzeit-Statistik, ohne Soll |

Die Feuerwehr definiert die Hilfsfrist als Zeit vom Beginn der Notrufabfrage in der Leitstelle bis zum Eintreffen der ersten Einsatzkräfte. Quellen: [Berliner Feuerwehr in Zahlen](https://www.berliner-feuerwehr.de/ueber-uns/berliner-feuerwehr-in-zahlen-2024-1/) (Frist, Soll und Ist je Einsatzart), [Senatsantwort 2019](https://pardok.parlament-berlin.de/starweb/adis/citat/VT/19/SchrAnfr/S19-19457.pdf), [Jahresbericht 2022](https://www.berliner-feuerwehr.de/fileadmin/bfw/dokumente/Publikationen/Jahresberichte_infografik/Infografik_Jahresbericht_2022_innen.pdf), [Jahresbericht 2023](https://www.berliner-feuerwehr.de/fileadmin/bfw/dokumente/Publikationen/Jahresberichte_infografik/Infografik_Jahresbericht_2023.pdf), [Open-Data-Seite der Feuerwehr](https://www.berliner-feuerwehr.de/service/open-data/). Den Gesetzestext haben wir nicht geprüft.

**Folgen für das Projekt**

- **Gesamtbetrachtungen sind immer nach Einsatzart aufgeschlüsselt.** Eine Zahl über alle Einsätze mischt Vorgaben, die nicht vergleichbar sind. Jede Auswertung zeigt zuerst das Gesamtbild und direkt daneben die Aufteilung in Rettungsdienst, Brandbekämpfung und technische Hilfeleistung, jeweils mit der passenden Frist (oder dem Hinweis, dass es keine gibt).
- **Die Hilfsfrist-Quote ist nur für den Rettungsdienst und die Brandbekämpfung definiert.** Die offizielle Quote in den Regionaldaten gilt nur für *kritische* Rettungsdiensteinsätze und für Brände.
- **"Kritisch" ist kein stabiler Begriff:** Seit dem 25.03.2025 klassifiziert die Feuerwehr Rettungsdiensteinsätze in Notfallkategorien (RD1 bis RD5). Die Zahl "kritischer" Einsätze fällt dadurch sprunghaft; Jahresvergleiche der Quote sind nur mit Vorsicht möglich.
- **Zwei Kennzahlen im Rettungsdienst:** die offizielle Quote (Regionaldaten, ab 2024) und unsere Näherung aus den Einzeleinsätzen (Dispatch-Stufen C/D/E, Schwelle 10 Minuten als Annahme); beide zeigt die App nebeneinander.
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
make dbt-build    # Seeds, Modelle, Tests (alle dbt-Befehle über make, sie setzen das Projektverzeichnis dbt/)
make export       # Marts nach public/app/data/ exportieren
make app          # Streamlit-Dashboard
```

`make help` listet alle Targets.

---

## Projektstruktur

```
.
├── dbt/             # Data Engineering: das vollständige dbt-Projekt (models, macros, seeds, tests, profiles.yml)
├── scripts/         # Data Engineering: Ingestion, Abrufe (LOR, Wachen, Codes), Parquet-Export
├── notebooks/       # Analysis und Science, nummeriert in Erzählreihenfolge
├── src/
│   ├── berlin_emergency_response/   # Python-Paket (Pfade, Hilfsfunktionen)
│   └── app/                         # Code der Streamlit-App
├── public/          # Web-Root (GitHub Pages) und Veröffentlichungen
│   └── app/data/    #   alle Daten der Live-App (Parquet, GeoJSON, insights.json)
├── data/            # DuckDB-Datei und Rohdaten (nicht versioniert)
├── tests/           # pytest für Python
├── docs/            # Plan, Konzept, Quellen, Datenwörterbuch
└── Makefile · pyproject.toml · uv.lock
```

`dbt/profiles.yml` ist versioniert: es enthält nur den lokalen DuckDB-Pfad, keine Zugangsdaten.

---

## Datenqualität

Tests liegen deklarativ in den `schema.yml` der dbt-Schichten (`unique`, `not_null`, `relationships`, `dbt_utils`) plus Singular Tests für fachliche Unmöglichkeiten. `dbt source freshness` prüft, ob Upstream-Daten pünktlich vorliegen.

---

## Lizenz und Datenquelle

Einsatzdaten: Berliner Feuerwehr, [BF-Open-Data](https://github.com/Berliner-Feuerwehr/BF-Open-Data), CC BY 4.0.
Wachen-Standorte: Berliner Feuerwehr, Geoportal Berlin (dl-de-zero-2.0).
Flächen: Amt für Statistik Berlin-Brandenburg / Statistische Einheiten im INSPIRE-Datenmodell (Lebensweltlich Orientierte Räume 01.01.2021), CC BY 3.0 DE.
