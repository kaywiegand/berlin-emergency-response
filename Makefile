# Makefile – berlin-emergency-response
# Verwendung: make <target>   (Voraussetzung: uv)

.PHONY: setup ingest ingest-full geo export notebooks test dbt-deps dbt-parse dbt-build app clean help

setup: ## Umgebung + Dependencies installieren
	uv sync
	uv run dbt deps

ingest: ## Tagesmodus: laufendes Jahr, Daily, Turnout-Snapshot
	uv run python scripts/ingest.py

ingest-full: ## Alle Jahre laden (rund 650 MB Download)
	uv run python scripts/ingest.py --full

geo: ## LOR-Polygone vom Geoportal laden und vereinfachen
	uv run python scripts/fetch_lor.py --refresh

export: ## Marts nach app_data/*.parquet exportieren
	uv run python scripts/export_parquet.py

notebooks: ## alle Notebooks ausführen (Outputs gespeichert)
	uv run jupyter nbconvert --to notebook --execute --inplace notebooks/*.ipynb

test: ## Python-Tests
	uv run pytest tests -q

dbt-deps: ## dbt-Packages installieren
	uv run dbt deps

dbt-parse: ## dbt-Projekt parsen (Syntaxcheck)
	uv run dbt parse

dbt-build: ## Seeds, Modelle, Snapshots und Tests ausführen
	uv run dbt build

app: ## Streamlit-App starten
	uv run streamlit run src/app.py

clean: ## Build-Artefakte und Caches entfernen
	rm -rf target logs .pytest_cache
	find . -type d -name __pycache__ -not -path "./.venv/*" -exec rm -rf {} + 2>/dev/null || true

help: ## Alle verfügbaren Targets anzeigen
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-12s %s\n", $$1, $$2}'
