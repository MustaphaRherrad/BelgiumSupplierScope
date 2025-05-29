# config/paths.py
from pathlib import Path

PROJECT_ROOT = Path(__file__).parents[2]  # Adapter selon la structure du projet
REPORTS_DIR = PROJECT_ROOT / "reports"
DATA_DIR = PROJECT_ROOT / "data"



""" EXEMPLES Utilsation

from config.paths import REPORTS_DIR

def save_data():
    output_path = REPORTS_DIR / "tables" / "expense" / "data.csv"
    output_path.parent.mkdir(exist_ok=True)

"""