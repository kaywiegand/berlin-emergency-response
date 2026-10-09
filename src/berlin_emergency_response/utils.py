"""
utils.py
--------
General helpers:
  - Timer decorator
  - File helpers
"""

import time
import logging
from pathlib import Path
from functools import wraps

logger = logging.getLogger(__name__)


def timer(func):
    """Decorator: measure and log the runtime of a function."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        logger.info(f"{func.__name__} finished in {elapsed:.2f}s")
        return result
    return wrapper


def ensure_dir(path: Path) -> Path:
    """Create the directory if it does not exist and return the path."""
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def list_files(directory: Path, pattern: str = "*") -> list[Path]:
    """Return all files in a directory matching the pattern, sorted."""
    return sorted(Path(directory).glob(pattern))
