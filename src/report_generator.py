from pathlib import Path
from datetime import datetime
import pandas as pd

def generate_markdown_report(alerts: pd.DataFrame, output: str | Path):
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)

    total = len(alerts)
    suspicious = int((alerts["classification"] != "NORMAL").sum())
    critical = int((alerts["severity"] == "CRITICAL").sum())
    high = int((alerts["severity"] == "HIGH").sum())

    top_sources = (
        alerts[alerts["classification"] != "NORMAL"]["src_ip"]
        .value_counts()
        .head(5)
        .to_dict()
    )

    lines = [
        "# IDS Incident Report",
        "",
        f"Generated: {datetime.now().isoformat(timespec='seconds')}",
        "",
        "## Executive Summary",
        f"- Total flow records analyzed: **{total}**",
        f"- Suspicious/potential intrusion records: **{suspicious}**",
        f"- High severity alerts: **{high}**",
        f"- Critical alerts: **{critical}**",
        "",
        "## Top Suspicious Sources",
    ]
    if top_sources:
        for src, count in top_sources.items():
            lines.append(f"- `{src}` — {count} alert(s)")
    else:
        lines.append("- No suspicious sources identified.")

    lines += [
        "",
        "## Highest Risk Events",
        "",
        "| Time | Source | Destination | Protocol | Classification | Severity | Risk | Rules |",
        "|---|---|---|---|---|---|---:|---|",
    ]

    for _, row in alerts.sort_values("risk_score", ascending=False).head(20).iterrows():
        lines.append(
            f"| {row.timestamp} | {row.src_ip} | {row.dst_ip} | "
            f"{row.protocol} | {row.classification} | {row.severity} | "
            f"{row.risk_score} | {row.rule_hits} |"
        )

    lines += [
        "",
        "## Defensive Interpretation",
        "The events above are generated from synthetic traffic records. "
        "They are detection-training artifacts and do not represent attacks against real systems.",
        "",
        "## Recommended Analyst Actions",
        "1. Validate whether the source is expected in the environment.",
        "2. Review the destination service and associated rule hits.",
        "3. Correlate repeated events from the same source.",
        "4. Escalate high/critical events according to the organization's incident-response process.",
        "5. Preserve evidence and document the analyst decision.",
    ]

    output.write_text("\n".join(lines), encoding="utf-8")
    return output
