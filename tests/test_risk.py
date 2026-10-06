from src.risk_engine import calculate_risk, severity_from_score, classification_from_score

def test_risk_is_capped():
    score = calculate_risk(100, 100, 100, ["A", "B", "C"])
    assert 0 <= score <= 100

def test_severity_boundaries():
    assert severity_from_score(10) == "INFO"
    assert severity_from_score(30) == "LOW"
    assert severity_from_score(50) == "MEDIUM"
    assert severity_from_score(70) == "HIGH"
    assert severity_from_score(90) == "CRITICAL"

def test_classification():
    assert classification_from_score(10) == "NORMAL"
    assert classification_from_score(40) == "SUSPICIOUS"
    assert classification_from_score(80) == "POTENTIAL INTRUSION"
