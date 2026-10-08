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
src/                 ← Streamlit-App + Plot-Utils
notebooks/           ← nach CONVENTIONS.md
public/              ← Web-Root (Pages), Quelle public/md/slides.yaml
docs/                ← PLAN, CONCEPT, DATA_SOURCES, DATA_DICTIONARY
```

---

## Konventionen

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
make app        # Streamlit
```
