import numpy as np
import pandas as pd

FEATURES = [
    "duration", "packets", "bytes_sent", "bytes_received",
    "failed_connections", "connection_rate", "src_port", "dst_port"
]

def apply_ml_detection(df: pd.DataFrame, enabled=True):
    result = df.copy()
    if not enabled:
        result["ml_score"] = 0.0
        result["ml_flag"] = False
        return result

    try:
        from sklearn.ensemble import IsolationForest
        X = result[FEATURES].astype(float).replace([np.inf, -np.inf], np.nan).fillna(0)
        model = IsolationForest(
            n_estimators=150,
            contamination=0.15,
            random_state=42
        )
        model.fit(X)
        decision = model.decision_function(X)
        # Convert lower decision values into higher anomaly scores.
        score = np.clip((0.15 - decision) * 100, 0, 100)
        result["ml_score"] = score.round(2)
        result["ml_flag"] = model.predict(X) == -1
        return result
    except Exception:
        result["ml_score"] = 0.0
        result["ml_flag"] = False
        return result
