def calculate_risk(rule_score, anomaly_score, ml_score, rule_hits):
    # Rule evidence is deliberately weighted most heavily for explainability.
    score = (
        float(rule_score) * 0.55
        + float(anomaly_score) * 0.30
        + float(ml_score) * 0.15
    )
    if len(rule_hits) >= 2:
        score += 8
    return round(min(max(score, 0), 100), 2)

def severity_from_score(score):
    if score >= 80:
        return "CRITICAL"
    if score >= 60:
        return "HIGH"
    if score >= 40:
        return "MEDIUM"
    if score >= 20:
        return "LOW"
    return "INFO"

def classification_from_score(score):
    if score >= 60:
        return "POTENTIAL INTRUSION"
    if score >= 25:
        return "SUSPICIOUS"
    return "NORMAL"
