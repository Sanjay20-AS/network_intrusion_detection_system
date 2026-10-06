from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
REPORT_DIR = BASE_DIR / "reports" / "generated"
DB_PATH = BASE_DIR / "ids_events.db"

for directory in (RAW_DIR, PROCESSED_DIR, REPORT_DIR):
    directory.mkdir(parents=True, exist_ok=True)

SEVERITIES = ["INFO", "LOW", "MEDIUM", "HIGH", "CRITICAL"]
CLASSIFICATIONS = ["NORMAL", "SUSPICIOUS", "POTENTIAL INTRUSION"]
