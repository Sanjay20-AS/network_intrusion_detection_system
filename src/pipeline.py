from pathlib import Path
import pandas as pd

from .ids_engine import run_ids, alert_frame
from .database import replace_alerts

def load_and_detect(input_path, enable_ml=True):
    df = pd.read_csv(input_path)
    result = run_ids(df, enable_ml=enable_ml)
    alerts = alert_frame(result)
    replace_alerts(alerts)
    return result, alerts

def save_results(result: pd.DataFrame, output_path):
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(output_path, index=False)
    return output_path
