# Concept — Berlin Emergency Response (dbt Certification Edition)

> Was gebaut wird, warum, und wie es als Vorbereitung auf die dbt Analytics Engineering Certification dient.
> Grundlage: [DATA_SOURCES.md](DATA_SOURCES.md).

---

## 1 · Worum es geht

Der Rettungsdienst hat eine gesetzlich definierte Frist, innerhalb derer er bei
einem kritischen Notfall vor Ort sein soll[cite: 1]. Ob diese Frist gehalten wird, ist
eine öffentlich diskutierte Frage[cite: 1]. Die Berliner Feuerwehr veröffentlicht die
nötigen Daten, aber die Kennzahl selbst wird nur jährlich und nur grob regional
ausgewiesen[cite: 1].

**Leitfrage**
Wie schnell ist der Rettungsdienst bei kritischen Notfällen tatsächlich vor Ort,
in welchen Bezirken wird die Hilfsfrist verfehlt, und wie verschiebt sich das
über die Jahre[cite: 1]?

**Abgrenzung — was dieses Projekt nicht ist**
Keine Bewertung der Einsatzkräfte[cite: 1]. Antwortzeiten hängen an Standortdichte,
Verkehr, Bebauung und Einsatzaufkommen, nicht an der Leistung einzelner Teams[cite: 1].
Das Projekt beschreibt Struktur, nicht Verschulden[cite: 1].

---

## 2 · Prüfungsabdeckung: dbt Analytics Engineering Certification

Dieses Projekt ist als lerneffektives Praxis-Beispiel aufgebaut[cite: 1], das alle 7 Hauptdomänen der offiziellen **dbt Analytics Engineering Certification** abdeckt:

| Prüfungsdomäne | Umsetzung im Projekt | Ordner / Datei |
| :--- | :--- | :--- |
| **1. Sources & Seeds** | Rohdaten-Definition, `source freshness` Warnschwellen & CSV-Seeds für Bezirkszuordnung | `models/staging/sources.yml`, `seeds/` |
| **2. Materializations** | Staging (`view`), Marts (`table`), Inkrementelles Laden von Einsätzen (`incremental`) | `models/staging/`, `models/marts/` |
| **3. Snapshots (SCD2)** | Historisierung von Fahrzeug-Kapazitäten & Wachen-Statusänderungen | `snapshots/` |
| **4. Testing & Quality** | Schema-Tests (`unique`, `relationships`) & Custom Singular SQL Tests | `models/schema.yml`, `tests/` |
| **5. Jinja & Macros** | Eigene UDF-Macros + Einbinden von `dbt-utils` | `macros/`, `packages.yml` |
| **6. Documentation** | `doc()` Blocks, Lineage DAG & Exposures (Evidence Dashboard Link) | `models/exposures.yml`, `doc_blocks.md` |
| **7. Execution & CLI** | `dbt build`, State-Selection, Tagging & Selector-Syntax (`+model+`) | Terminal / CI Commands |

---

## 3 · Architektur

````
BF-Open-Data (GitHub)
│  gezielt einzelne Raw-Dateien, kein Clone (Upstream ist 6,8 GB)
▼
Ingestion (Python)  ──►  data/raw/  mit Ladezeitpunkt
│
▼
DuckDB  ◄── dbt: staging → intermediate → marts
│           │
│           ├── Snapshots (SCD Type 2 Wachen-Status)
│           ├── Custom Macros & dbt-utils
│           └── Generic + Singular SQL Quality Tests
▼
Dashboard (Evidence.dev)  ──►  GitHub Pages
│
└── CI: dbt build bei jedem Pull Request
````

| Schicht | Werkzeug | Begründung |
| :--- | :--- | :--- |
| Orchestrierung | GitHub Actions | Cron ohne Server, Läufe öffentlich einsehbar[cite: 1] |
| Ingestion | Python, httpx | gezielter Abruf, Upstream-Clone verbietet sich[cite: 1] |
| Warehouse | DuckDB | eine Datei, SQL-vollständig, 600 MB problemlos[cite: 1] |
| Transformation | dbt-core | eigentlicher Zweck: Layering, Tests, Lineage[cite: 1] |
| Serving | Evidence.dev | SQL-natives BI, statisches HTML[cite: 1] |
| CI | GitHub Actions | `dbt build` je Pull Request[cite: 1] |

---

## 4 · Modell-Layer (dbt)

- **staging** — `views` je Quelldatei[cite: 1]. Nur Umbenennung, Typisierung, Zeitzone[cite: 1].
- **intermediate** — Einsätze auf Tag und Bezirk verdichtet, Hilfsfrist-Flag je Einsatz via Jinja-Macro[cite: 1].
- **marts** — `tables` und `incremental models`: `fct_missions_daily`, `fct_response_times`, `dim_district`[cite: 1].

---

## 5 · Qualitätssicherung

- Standardtests auf Schlüssel, Pflichtfelder, Wertebereiche[cite: 1]
- Custom Singular SQL Tests auf fachliche Unmöglichkeiten (negative Antwortzeiten, Quoten > 100%)[cite: 1]
- `source freshness` prüft, ob Upstream-Daten pünktlich vorliegen[cite: 1]

---

## 6 · Erfolgskriterien & Risiken

1. Pipeline läuft täglich via GitHub Actions automatisiert[cite: 1].
2. Hilfsfrist-Definition ist nachvollziehbar dokumentiert und im Modell umgesetzt[cite: 1].
3. Upstream-Daten werden gezielt ohne 6,8 GB Repository-Clone eingebunden[cite: 1, 2].