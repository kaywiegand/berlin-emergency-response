# CLAUDE.md — Berlin Emergency Response

> Projektspezifische Anweisungen für Claude Code.
> Ergänzt die globale CLAUDE.md aus dem Workspace-Root.

---

## Projekt

| Feld | Inhalt |
| :--- | :--- |
| Slug | `berlin-emergency-response` |
| Typ | DE — Data / Analytics Engineering (Scaffolding-Typ `DA`, angepasst) |
| Ziel | Portfolio-Case + dbt-Analytics-Engineering-Zertifizierung |
| Stack | Python (httpx, pandas) · DuckDB · dbt-core (`dbt-duckdb`, `dbt_utils`) · Streamlit · Plotly · `wgnd` · uv |
| Daten | Berliner Feuerwehr Open Data (CC BY 4.0) → `docs/DATA_SOURCES.md` |

---

## Session-Einstieg

```
1. PROCESS_LOG.md lesen — aktueller Stand und letzte Session
2. docs/PLAN.md lesen — Schritte S0–S6
3. ROADMAP.md · BACKLOG.md
4. Globale CLAUDE.md aus /Users/kaywiegand/Workspace/ gilt weiterhin
```

---

## Struktur

```
dbt/                 ← Data Engineering: dbt-Projekt (models, macros, seeds, tests, profiles.yml)
scripts/             ← Ingestion, Abrufe (LOR, Wachen, Codes), Parquet-Export
notebooks/           ← Analysis + Science, nummeriert (CONVENTIONS.md)
src/berlin_emergency_response/ ← Python-Paket (config, settings, notebook, spatial)
src/app/             ← Streamlit-App-Code (liest nur public/app/data/)
public/              ← Web-Root (Pages); public/app/data/ = alle Daten der Live-App; Quelle public/md/slides.yaml
data/raw/, data/*.duckdb, data/models/ ← Rohdaten, Warehouse, später ML-Modelle (ignoriert)
tests/               ← pytest (Python); dbt-Tests liegen in dbt/tests/ und dbt/models/**/schema.yml
docs/                ← PLAN, CONCEPT, DATA_SOURCES, DATA_DICTIONARY
```

---

## Konventionen

- **Differenzierung nach Einsatzart (Pflicht):** Jede Gesamtbetrachtung (Notebook, Mart, App) zeigt zusätzlich die Aufschlüsselung nach Einsatzart (Rettungsdienst, Brandbekämpfung, technische Hilfeleistung). Die Vorgaben unterscheiden sich (RD: 10 min, Brand: 14 Funktionen in 15 min, technische Hilfe: keine Frist vereinbart), siehe README "Fristen und Schutzziele". Schwellen gelten je Einsatzart, nie global.
- Code, Spalten, Kommentare: Englisch. Markdown: Deutsch.
- dbt-Schichten: `stg_` (view) → `int_` (view) → `fct_`/`dim_` (table/incremental).
- dbt-Befehle immer über `make` (setzt `DBT_PROJECT_DIR=dbt`, `DBT_PROFILES_DIR=dbt`); `dbt/profiles.yml` liegt im Repo (nur lokaler DuckDB-Pfad, keine Secrets). Secrets nie dort ablegen.
- `wgnd` kommt per Git-URL aus `wgnd-toolkit` (Dependency, kein lokaler Fork).
- Hypothesen als "Vermutung" markieren (siehe offene Verifikationen in `docs/PLAN.md`).

---

## Befehle

```bash
make setup      # uv sync + dbt deps
make dbt-build  # dbt build
make dbt-parse  # Syntaxcheck
make export     # Marts -> public/app/data/*.parquet
make geo        # LOR-Polygone (selten nötig)
make stations   # Wachen-Standorte und Einsatzbereiche (selten nötig)
make app        # Streamlit
```
