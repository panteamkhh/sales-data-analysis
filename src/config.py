"""Central project paths and constants.

All paths are resolved relative to the repository root so scripts and the
notebook behave the same regardless of the current working directory.
"""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_FILE = PROJECT_ROOT / "data" / "store_data.xlsx"
SCREENSHOTS_DIR = PROJECT_ROOT / "screenshots"
OUTPUT_DIR = PROJECT_ROOT / "output"
POWERBI_DIR = PROJECT_ROOT / "powerbi"

# Flat profit margin applied to Net Sales. The source data has no cost column,
# so profit is estimated rather than measured (matches the Power BI model).
PROFIT_MARGIN = 0.10

__all__ = [
    "PROJECT_ROOT",
    "DATA_FILE",
    "SCREENSHOTS_DIR",
    "OUTPUT_DIR",
    "POWERBI_DIR",
    "PROFIT_MARGIN",
]
