from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.database import load_alerts
from src.report_generator import generate_markdown_report

alerts = load_alerts()
path = generate_markdown_report(alerts, "reports/generated/incident_report.md")
print(f"Report -> {path}")
