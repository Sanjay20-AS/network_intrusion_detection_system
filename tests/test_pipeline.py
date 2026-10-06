from src.traffic_generator import generate_dataset
from src.ids_engine import run_ids

def test_pipeline_shape():
    df = generate_dataset(100, seed=1)
    result = run_ids(df, enable_ml=False)
    required = {
        "risk_score", "severity", "classification",
        "rule_hits", "anomaly_score", "ml_score"
    }
    assert required.issubset(result.columns)
    assert len(result) == 100
