# Berlin Emergency Response

> **Typ:** DA &nbsp;|&nbsp; **Erstellt:** 2026-08-30 &nbsp;|&nbsp; **Version:** 0.1.0

---

## Schnellstart

### 1. Virtuelle Umgebung erstellen & aktivieren

```bash
uv venv
source .venv/bin/activate   # Mac/Linux
.venv\Scripts\activate      # Windows
```

### 2. Dependencies + Projektpaket installieren

```bash
uv pip install -e ".[da]"
```

### 3. Jupyter Kernel registrieren

```bash
python -m ipykernel install --user --name berlin_emergency_response --display-name "Python (berlin_emergency_response)"
```

Oder einfach: `make setup && make kernel`

### 4. Los geht's!

Oeffne `notebooks/00_introduction.ipynb` und fange an.

---

## Projektstruktur

```
berlin-emergency-response/
|
+-- PROCESS_LOG.md          # Projektverlauf & AI-Kontext-Einstieg
+-- ROADMAP.md              # Phasen & offene Tasks
+-- CLAUDE.md               # Claude Code Anweisungen
+-- README.md
+-- pyproject.toml          # Paketkonfiguration & Dependencies
+-- Makefile                # Shortcuts (make setup, make kernel, ...)
+-- .gitignore
|
+-- data/                   # NICHT in Git! (.gitignore)
|   +-- raw/                # Rohdaten - NIEMALS veraendern!
|   +-- interim/            # Zwischenergebnisse
|   +-- processed/          # Finale, analysefertige Daten
|
+-- notebooks/
|   +-- 00_introduction.ipynb
|   +-- 01_exploration.ipynb
|   +-- 02_preparation.ipynb
|   +-- 03_analysis.ipynb
|   +-- 04_insights.ipynb
|
+-- src/berlin_emergency_response/     # Python-Paket (importierbar nach uv install)
|   +-- config.py           # Zentrale Pfade & Konstanten
|   +-- settings.py         # Plot-Theme, Logging
|   +-- notebook.py         # Zentraler Import-Einstieg fuer Notebooks
|   +-- utils.py            # Hilfsfunktionen
|   +-- data/
|   +-- features/
|   +-- visualization/
|   +-- analytics/
|
+-- tests/
+-- public/
    +-- index.html
    +-- img/
    +-- md/
```

---

## Notebooks

In Lesereihenfolge:

| Notebook | Zweck |
| :--- | :--- |
| [`00_introduction`](notebooks/00_introduction.ipynb) | Projekt-Facts, Kontext, Workflow, Conventions |
| [`01_exploration`](notebooks/01_exploration.ipynb) | EDA + Discovery |
| [`02_preparation`](notebooks/02_preparation.ipynb) | Preparation + Preprocessing, Export |
| [`03_analysis`](notebooks/03_analysis.ipynb) | Import, Analysis + Analytics |
| [`04_insights`](notebooks/04_insights.ipynb) | Business Communication + Insights |

---

## Report

Öffentlicher Einstieg / Präsentation: [`public/index.html`](public/index.html) — Landing-Page mit Navigation zu den Report-Views.

> Start als Platzhalter, wird über `/project-case` mit Inhalt gefüllt (Story, Slides, Views).

---

## Konfiguration

### Pfade (`src/berlin_emergency_response/config.py`)

```python
from berlin_emergency_response.config import PATHS

PATHS["raw"]       # data/raw/
PATHS["processed"] # data/processed/
PATHS["figures"]   # public/img/
```

### Notebook-Einstieg

```python
from berlin_emergency_response.notebook import *
setup_plotting()
```

---

## Tests ausfuehren

```bash
pytest
pytest --cov=src/berlin_emergency_response --cov-report=term-missing
```

---

_Generiert mit dem wgnd-scaffolding Generator._
