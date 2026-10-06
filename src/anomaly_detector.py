import numpy as np
import pandas as pd

FEATURES = [
    "duration", "packets", "bytes_sent", "bytes_received",
    "failed_connections", "connection_rate"
]

def _robust_z(series):
    median = series.median()
    mad = (series - median).abs().median()
    if mad == 0:
        std = series.std()
        return (series - median) / (std if std and std > 0 else 1)
    return 0.6745 * (series - median) / mad

def anomaly_scores(df: pd.DataFrame):
    z = pd.DataFrame(index=df.index)
    for feature in FEATURES:
        z[feature] = _robust_z(pd.to_numeric(df[feature]))
    magnitude = z.abs().mean(axis=1)
    score = np.clip(magnitude * 18, 0, 100)
    return score.round(2)

def apply_anomaly_detection(df):
    result = df.copy()
    result["anomaly_score"] = anomaly_scores(result)
    result["anomaly_flag"] = result["anomaly_score"] >= 55
    return result
