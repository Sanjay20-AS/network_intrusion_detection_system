import argparse
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.pipeline import load_and_detect, save_results

parser = argparse.ArgumentParser(description="Run the defensive IDS simulation.")
parser.add_argument("--input", default="data/raw/network_flows.csv")
parser.add_argument("--output", default="data/processed/detected_flows.csv")
parser.add_argument("--no-ml", action="store_true")
args = parser.parse_args()

result, alerts = load_and_detect(args.input, enable_ml=not args.no_ml)
save_results(result, args.output)

print(f"Analyzed: {len(result)}")
print(f"Suspicious: {(result['classification'] != 'NORMAL').sum()}")
print(f"High/Critical: {(result['severity'].isin(['HIGH', 'CRITICAL'])).sum()}")
print(f"Results -> {args.output}")
