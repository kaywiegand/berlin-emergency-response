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
data/raw/            ← Rohdaten, schreibgeschützt (ignoriert)
data/*.duckdb        ← Warehouse (ignoriert)
models/              ← dbt: staging → intermediate → marts
seeds/ macros/ snapshots/ tests/   ← dbt
scripts/             ← Ingestion
src/app.py, src/utils/ ← Streamlit-App (liest nur app_data/)
src/berlin_emergency_response/ ← Projektpaket für Notebooks (config, settings, notebook)
app_data/            ← Parquet-Export + geo/ (versioniert, von der App gelesen)
notebooks/           ← nach CONVENTIONS.md
public/              ← Web-Root (Pages), Quelle public/md/slides.yaml
docs/                ← PLAN, CONCEPT, DATA_SOURCES, DATA_DICTIONARY
```

---

## Konventionen

- **Differenzierung nach Einsatzart (Pflicht):** Jede Gesamtbetrachtung (Notebook, Mart, App) zeigt zusätzlich die Aufschlüsselung nach Einsatzart (Rettungsdienst, Brandbekämpfung, technische Hilfeleistung). Die Vorgaben unterscheiden sich (RD: 10 min, Brand: 14 Funktionen in 15 min, technische Hilfe: keine Frist gefunden), siehe README "Fristen und Schutzziele". Schwellen gelten je Einsatzart, nie global.
- Code, Spalten, Kommentare: Englisch. Markdown: Deutsch.
- dbt-Schichten: `stg_` (view) → `int_` (view) → `fct_`/`dim_` (table/incremental).
- `profiles.yml` liegt im Repo (nur lokaler DuckDB-Pfad, keine Secrets). Secrets nie dort ablegen.
- `wgnd` kommt per Git-URL aus `wgnd-toolkit` (Dependency, kein lokaler Fork).
- Hypothesen als "Vermutung" markieren (siehe offene Verifikationen in `docs/PLAN.md`).

---

## Befehle

```bash
make setup      # uv sync + dbt deps
make dbt-build  # dbt build
make dbt-parse  # Syntaxcheck
make export     # Marts -> app_data/*.parquet
make geo        # LOR-Polygone (selten nötig)
make stations   # Wachen-Standorte und Einsatzbereiche (selten nötig)
make app        # Streamlit
```
