import pandas as pd

from .rule_engine import apply_rules
from .anomaly_detector import apply_anomaly_detection
from .ml_detector import apply_ml_detection
from .risk_engine import calculate_risk, severity_from_score, classification_from_score

def run_ids(df: pd.DataFrame, enable_ml=True):
    result = df.copy()

    rules = apply_rules(result)
    result = pd.concat([result, rules], axis=1)
    result = apply_anomaly_detection(result)
    result = apply_ml_detection(result, enabled=enable_ml)

    risks, severities, classifications = [], [], []
    reason_text, hit_text = [], []

    for _, row in result.iterrows():
        hits = row["hits"]
        reasons = row["reasons"]
        risk = calculate_risk(
            row["rule_score"],
            row["anomaly_score"],
            row["ml_score"],
            hits
        )
        risks.append(risk)
        severities.append(severity_from_score(risk))
        classifications.append(classification_from_score(risk))
        reason_text.append("; ".join(reasons) if reasons else "No strong rule evidence")
        hit_text.append(", ".join(hits) if hits else "NONE")

    result["risk_score"] = risks
    result["severity"] = severities
    result["classification"] = classifications
    result["reasons"] = reason_text
    result["rule_hits"] = hit_text
    result.drop(columns=["hits"], inplace=True, errors="ignore")
    return result

def alert_frame(result: pd.DataFrame):
    cols = [
        "timestamp", "src_ip", "dst_ip", "protocol", "src_port", "dst_port",
        "classification", "severity", "risk_score", "reasons", "rule_hits",
        "anomaly_score", "ml_score"
    ]
    return result[cols].copy()
