import sqlite3
from pathlib import Path
import pandas as pd

from .config import DB_PATH

CREATE_SQL = """
CREATE TABLE IF NOT EXISTS alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    src_ip TEXT NOT NULL,
    dst_ip TEXT NOT NULL,
    protocol TEXT NOT NULL,
    src_port INTEGER,
    dst_port INTEGER,
    classification TEXT NOT NULL,
    severity TEXT NOT NULL,
    risk_score REAL NOT NULL,
    reasons TEXT,
    rule_hits TEXT,
    anomaly_score REAL,
    ml_score REAL
)
"""

def get_connection(path: str | Path = DB_PATH):
    conn = sqlite3.connect(path)
    conn.execute(CREATE_SQL)
    return conn

def replace_alerts(alerts_df: pd.DataFrame, path: str | Path = DB_PATH):
    conn = get_connection(path)
    conn.execute("DELETE FROM alerts")
    cols = [
        "timestamp", "src_ip", "dst_ip", "protocol", "src_port", "dst_port",
        "classification", "severity", "risk_score", "reasons", "rule_hits",
        "anomaly_score", "ml_score"
    ]
    alerts_df[cols].to_sql("alerts", conn, if_exists="append", index=False)
    conn.commit()
    conn.close()

def load_alerts(path: str | Path = DB_PATH):
    conn = get_connection(path)
    df = pd.read_sql_query("SELECT * FROM alerts ORDER BY risk_score DESC", conn)
    conn.close()
    return df
