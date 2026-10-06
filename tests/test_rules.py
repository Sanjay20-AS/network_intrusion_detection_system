import pandas as pd
from src.rule_engine import evaluate_row

def test_high_connection_rate_rule():
    row = pd.Series({
        "connection_rate": 250,
        "failed_connections": 0,
        "dst_port": 443,
        "protocol": "TCP",
        "packets": 20,
        "bytes_sent": 100,
        "bytes_received": 100,
    })
    result = evaluate_row(row)
    assert "HIGH_CONNECTION_RATE" in result["hits"]
    assert result["score"] >= 28

def test_unusual_port_rule():
    row = pd.Series({
        "connection_rate": 1,
        "failed_connections": 0,
        "dst_port": 4444,
        "protocol": "TCP",
        "packets": 10,
        "bytes_sent": 100,
        "bytes_received": 100,
    })
    result = evaluate_row(row)
    assert "UNUSUAL_DESTINATION_PORT" in result["hits"]
