"""
notebook.py
-----------
Single entry point for all notebooks.
Import once at the top of every notebook:

    from berlin_emergency_response.notebook import *
    setup_plotting()
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

from wgnd.inspect import (
    inspect,
    inspect_missing,
    inspect_duplicates,
    inspect_outliers,
    inspect_outlier_detail,
    inspect_correlations,
)
from wgnd.core._output import success, warn, log, info_box, show_df, section_header
from wgnd.core.config import cfg

from berlin_emergency_response.config import PATHS, PROJECT_NAME, RANDOM_SEED
from berlin_emergency_response.settings import setup_plotting

__all__ = [
    "pd", "np", "plt", "sns", "Path",
    "inspect", "inspect_missing", "inspect_duplicates",
    "inspect_outliers", "inspect_outlier_detail", "inspect_correlations",
    "success", "warn", "log", "info_box", "show_df", "section_header", "cfg",
    "PATHS", "PROJECT_NAME", "RANDOM_SEED", "setup_plotting",
]
