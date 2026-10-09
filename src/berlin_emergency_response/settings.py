"""
settings.py
-----------
Visual and logging configuration:
  - wgnd theme (Matplotlib / Seaborn)
  - Color palettes
  - Logging format
"""

import logging
import matplotlib.pyplot as plt
import seaborn as sns

# ─── Colors ────────────────────────────────────────────────────────────────
PALETTE_PRIMARY  = ["#2E86AB", "#A23B72", "#F18F01", "#C73E1D", "#3B1F2B"]
PALETTE_SEABORN  = "muted"

# ─── Plot style ─────────────────────────────────────────────────────────────
FIGSIZE_DEFAULT  = (10, 6)
FIGSIZE_WIDE     = (14, 6)
DPI              = 120


def setup_plotting() -> None:
    """Apply the wgnd theme, notebook display options and autoreload."""
    import pandas as pd
    from wgnd.core.theme import setup as wgnd_setup

    wgnd_setup()
    plt.rcParams.update({
        "figure.figsize": FIGSIZE_DEFAULT,
        "figure.dpi":     DPI,
    })
    pd.set_option("display.notebook_repr_html", True)
    pd.set_option("display.max_rows", 10)
    pd.set_option("display.max_columns", None)

    try:
        from IPython import get_ipython
        ip = get_ipython()
        if ip:
            ip.run_line_magic("load_ext", "autoreload")
            ip.run_line_magic("autoreload", "2")
    except Exception:
        pass


# ─── Logging ───────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("project")
