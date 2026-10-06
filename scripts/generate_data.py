import argparse
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.traffic_generator import generate_dataset, save_dataset

parser = argparse.ArgumentParser(description="Generate safe synthetic network-flow records.")
parser.add_argument("--rows", type=int, default=1000)
parser.add_argument("--output", default="data/raw/network_flows.csv")
args = parser.parse_args()

df = generate_dataset(args.rows)
save_dataset(df, args.output)
print(f"Generated {len(df)} synthetic flow records -> {args.output}")
