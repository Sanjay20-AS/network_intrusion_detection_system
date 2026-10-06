import random
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

NORMAL_PORTS = [53, 80, 443, 22, 123, 25, 110, 143, 8080]
UNUSUAL_PORTS = [23, 135, 139, 445, 31337, 4444, 9999]

def _ip(private=True):
    if private:
        return f"10.0.{random.randint(0, 10)}.{random.randint(2, 254)}"
    return f"192.0.2.{random.randint(1, 254)}"  # documentation/test network

def _normal_row(ts):
    protocol = random.choices(["TCP", "UDP", "ICMP"], weights=[65, 28, 7])[0]
    if protocol == "ICMP":
        src_port, dst_port = 0, 0
        packets = random.randint(1, 20)
    else:
        src_port = random.randint(1024, 65535)
        dst_port = random.choice(NORMAL_PORTS)
        packets = random.randint(2, 80)

    duration = round(random.uniform(0.02, 8), 3)
    bytes_sent = int(np.random.lognormal(7.3, 0.8))
    bytes_recv = int(np.random.lognormal(7.2, 0.8))

    return {
        "timestamp": ts.isoformat(),
        "src_ip": _ip(),
        "dst_ip": _ip(private=False),
        "protocol": protocol,
        "src_port": src_port,
        "dst_port": dst_port,
        "duration": duration,
        "packets": packets,
        "bytes_sent": bytes_sent,
        "bytes_received": bytes_recv,
        "failed_connections": 0,
        "connection_rate": round(random.uniform(0.2, 25), 2),
        "label": "NORMAL",
    }

def _attack_like_row(ts, kind):
    src = _ip()
    dst = _ip(private=False)

    if kind == "port_anomaly":
        protocol = "TCP"
        src_port = random.randint(30000, 65000)
        dst_port = random.choice(UNUSUAL_PORTS)
        packets = random.randint(30, 100)
        rate = random.uniform(40, 100)
        failed = random.randint(1, 5)
        bs, br = random.randint(2000, 15000), random.randint(1000, 8000)
    elif kind == "connection_burst":
        protocol = "TCP"
        src_port = random.randint(30000, 65000)
        dst_port = random.choice([22, 80, 443])
        packets = random.randint(80, 250)
        rate = random.uniform(120, 500)
        failed = random.randint(5, 30)
        bs, br = random.randint(1000, 9000), random.randint(500, 4000)
    elif kind == "icmp_flood_like":
        protocol = "ICMP"
        src_port = dst_port = 0
        packets = random.randint(150, 500)
        rate = random.uniform(80, 350)
        failed = 0
        bs, br = random.randint(10000, 80000), random.randint(5000, 30000)
    else:  # large transfer
        protocol = "TCP"
        src_port = random.randint(30000, 65000)
        dst_port = random.choice([80, 443])
        packets = random.randint(50, 160)
        rate = random.uniform(10, 60)
        failed = random.randint(0, 3)
        bs, br = random.randint(500000, 3000000), random.randint(100000, 1000000)

    return {
        "timestamp": ts.isoformat(),
        "src_ip": src,
        "dst_ip": dst,
        "protocol": protocol,
        "src_port": src_port,
        "dst_port": dst_port,
        "duration": round(random.uniform(0.01, 2), 3),
        "packets": packets,
        "bytes_sent": bs,
        "bytes_received": br,
        "failed_connections": failed,
        "connection_rate": round(rate, 2),
        "label": kind.upper(),
    }

def generate_dataset(rows=1000, seed=42):
    random.seed(seed)
    np.random.seed(seed)
    start = datetime.now().replace(microsecond=0) - timedelta(minutes=30)
    attack_kinds = ["port_anomaly", "connection_burst", "icmp_flood_like", "large_transfer"]
    records = []

    for i in range(rows):
        ts = start + timedelta(seconds=i * 2)
        if random.random() < 0.18:
            record = _attack_like_row(ts, random.choice(attack_kinds))
        else:
            record = _normal_row(ts)
        records.append(record)

    return pd.DataFrame(records)

def save_dataset(df: pd.DataFrame, output: str | Path):
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output, index=False)
    return output
