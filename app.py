import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import pandas as pd
import plotly.express as px
import streamlit as st

from src.config import DB_PATH
from src.database import load_alerts
from src.traffic_generator import generate_dataset, save_dataset
from src.pipeline import load_and_detect, save_results
from src.report_generator import generate_markdown_report

st.set_page_config(page_title="IDS Simulation SOC", page_icon="🛡️", layout="wide")

st.title("🛡️ Network Intrusion Detection System")
st.caption("Defensive, synthetic-flow IDS simulation — no external network traffic is generated.")

with st.sidebar:
    st.header("Simulation Controls")
    rows = st.slider("Synthetic flow records", 100, 5000, 1000, step=100)
    use_ml = st.checkbox("Enable Isolation Forest ML", value=True)

    if st.button("Generate + Detect", type="primary"):
        df = generate_dataset(rows)
        save_dataset(df, "data/raw/network_flows.csv")
        result, alerts = load_and_detect("data/raw/network_flows.csv", enable_ml=use_ml)
        save_results(result, "data/processed/detected_flows.csv")
        st.session_state["ran"] = True
        st.success(f"Analyzed {len(result)} records.")

try:
    alerts = load_alerts()
except Exception:
    alerts = pd.DataFrame()

if alerts.empty:
    st.info("No results yet. Use **Generate + Detect** in the sidebar.")
    st.stop()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Flows analyzed", len(alerts))
c2.metric("Suspicious", int((alerts.classification != "NORMAL").sum()))
c3.metric("High", int((alerts.severity == "HIGH").sum()))
c4.metric("Critical", int((alerts.severity == "CRITICAL").sum()))

st.divider()

left, right = st.columns(2)
with left:
    sev = alerts["severity"].value_counts().reset_index()
    sev.columns = ["severity", "count"]
    st.plotly_chart(px.bar(sev, x="severity", y="count", title="Alerts by Severity"), use_container_width=True)

with right:
    cls = alerts["classification"].value_counts().reset_index()
    cls.columns = ["classification", "count"]
    st.plotly_chart(px.pie(cls, names="classification", values="count", title="Traffic Classification"), use_container_width=True)

st.subheader("Traffic Analytics")
p1, p2 = st.columns(2)

with p1:
    proto = alerts["protocol"].value_counts().reset_index()
    proto.columns = ["protocol", "count"]
    st.plotly_chart(px.bar(proto, x="protocol", y="count", title="Protocol Distribution"), use_container_width=True)

with p2:
    st.plotly_chart(
        px.histogram(alerts, x="risk_score", nbins=20, title="Risk Score Distribution"),
        use_container_width=True,
    )

st.subheader("SOC Investigation")
filter_sev = st.multiselect(
    "Severity filter",
    ["INFO", "LOW", "MEDIUM", "HIGH", "CRITICAL"],
    default=["LOW", "MEDIUM", "HIGH", "CRITICAL"]
)

filtered = alerts[alerts["severity"].isin(filter_sev)].sort_values("risk_score", ascending=False)

st.dataframe(
    filtered[
        ["timestamp", "src_ip", "dst_ip", "protocol", "dst_port",
         "classification", "severity", "risk_score", "rule_hits", "reasons"]
    ],
    use_container_width=True,
    hide_index=True,
)

st.subheader("Incident Report")
if st.button("Generate Markdown Incident Report"):
    path = generate_markdown_report(alerts, "reports/generated/incident_report.md")
    st.success(f"Report generated: {path}")

csv_data = filtered.to_csv(index=False).encode("utf-8")
st.download_button(
    "Export Filtered Alerts CSV",
    data=csv_data,
    file_name="ids_alerts.csv",
    mime="text/csv"
)

st.caption(f"SQLite event store: {DB_PATH}")
