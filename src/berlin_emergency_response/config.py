"""
config.py
---------
Central project configuration: paths and constants.

    from berlin_emergency_response.config import PATHS, PROJECT_NAME
"""

from pathlib import Path

PROJECT_NAME = "Berlin Emergency Response"
RANDOM_SEED = 42

# config.py lives in src/<package>/, the project root is three levels up
_ROOT = Path(__file__).resolve().parent.parent.parent

PATHS = {
    "root":      _ROOT,
    "data":      _ROOT / "data",
    "raw":       _ROOT / "data" / "raw",
    "db":        _ROOT / "data" / "berlin_emergency.duckdb",
    "dbt_models": _ROOT / "models",
    "app_data":  _ROOT / "app_data",
    "public":    _ROOT / "public",
    "figures":   _ROOT / "public" / "img",
}
