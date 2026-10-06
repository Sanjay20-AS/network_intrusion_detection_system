import pandas as pd

UNUSUAL_PORTS = {23, 135, 139, 445, 31337, 4444, 9999}

RULES = {
    "HIGH_CONNECTION_RATE": {"threshold": 100, "weight": 28},
    "REPEATED_FAILURES": {"threshold": 5, "weight": 22},
    "UNUSUAL_DESTINATION_PORT": {"weight": 20},
    "ICMP_VOLUME_SPIKE": {"threshold": 120, "weight": 25},
    "LARGE_DATA_TRANSFER": {"threshold": 1_000_000, "weight": 18},
}

def evaluate_row(row):
    hits, reasons, score = [], [], 0

    if float(row["connection_rate"]) > RULES["HIGH_CONNECTION_RATE"]["threshold"]:
        hits.append("HIGH_CONNECTION_RATE")
        reasons.append("Connection rate is unusually high")
        score += RULES["HIGH_CONNECTION_RATE"]["weight"]

    if int(row["failed_connections"]) >= RULES["REPEATED_FAILURES"]["threshold"]:
        hits.append("REPEATED_FAILURES")
        reasons.append("Repeated failed connections detected")
        score += RULES["REPEATED_FAILURES"]["weight"]

    if int(row["dst_port"]) in UNUSUAL_PORTS:
        hits.append("UNUSUAL_DESTINATION_PORT")
        reasons.append(f"Destination port {int(row['dst_port'])} is unusual in this lab profile")
        score += RULES["UNUSUAL_DESTINATION_PORT"]["weight"]

    if row["protocol"] == "ICMP" and int(row["packets"]) > RULES["ICMP_VOLUME_SPIKE"]["threshold"]:
        hits.append("ICMP_VOLUME_SPIKE")
        reasons.append("ICMP packet volume is unusually high")
        score += RULES["ICMP_VOLUME_SPIKE"]["weight"]

    total_bytes = int(row["bytes_sent"]) + int(row["bytes_received"])
    if total_bytes > RULES["LARGE_DATA_TRANSFER"]["threshold"]:
        hits.append("LARGE_DATA_TRANSFER")
        reasons.append("Flow transferred an unusually large amount of data")
        score += RULES["LARGE_DATA_TRANSFER"]["weight"]

    return {"score": min(score, 100), "hits": hits, "reasons": reasons}

def apply_rules(df: pd.DataFrame):
    results = df.apply(evaluate_row, axis=1)
    out = pd.DataFrame(results.tolist(), index=df.index)
    out["rule_score"] = out["score"]
    return out.drop(columns=["score"])
