from dataclasses import dataclass, asdict
from typing import Any

@dataclass
class Alert:
    timestamp: str
    src_ip: str
    dst_ip: str
    protocol: str
    src_port: int
    dst_port: int
    classification: str
    severity: str
    risk_score: float
    reasons: str
    rule_hits: str
    anomaly_score: float
    ml_score: float

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
