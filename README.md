# Network Intrusion Detection System (IDS) Simulation

A beginner-friendly, defensive cybersecurity project that simulates network-flow records and detects suspicious activity using signature/rule-based detection, statistical anomaly detection, and an optional machine-learning model.

> **Safety:** This project is designed for offline/local defensive learning. It does not scan, probe, exploit, or attack public or third-party systems. The traffic is synthetic JSON/CSV data representing flows.

## Features

- Synthetic network-flow dataset generator
- Controlled traffic simulator with normal and attack-like *records* only
- Rule/signature-based detection
- Statistical anomaly detection
- Optional Isolation Forest ML detector
- Risk scoring and severity classification
- SQLite security-event storage
- SOC-style alert investigation
- Streamlit dashboard
- CSV/JSON incident report generation
- Unit tests
- CLI workflow
- Docker support
- GitHub-ready structure

## Detection classes

- `NORMAL`
- `SUSPICIOUS`
- `POTENTIAL INTRUSION`

## Alert severities

- `INFO`
- `LOW`
- `MEDIUM`
- `HIGH`
- `CRITICAL`

## Architecture

```text
Synthetic Traffic Generator
          |
          v
   Network Flow Records
          |
          v
      IDS Engine
      /    |     \
     /     |      \
 Rules  Anomaly    ML
  |       |         |
  +-------+---------+
          |
          v
    Risk / Severity
          |
          v
    Alert + Database
          |
          +----------------+
          |                |
          v                v
    SOC Dashboard     Incident Reports
```

## Project structure

```text
network_intrusion_detection_system/
├── app.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .gitignore
├── LICENSE
├── README.md
├── data/
│   ├── raw/
│   └── processed/
├── reports/
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── database.py
│   ├── schemas.py
│   ├── traffic_generator.py
│   ├── rule_engine.py
│   ├── anomaly_detector.py
│   ├── ml_detector.py
│   ├── risk_engine.py
│   ├── ids_engine.py
│   ├── report_generator.py
│   └── pipeline.py
├── scripts/
│   ├── generate_data.py
│   ├── run_detection.py
│   └── generate_report.py
└── tests/
    ├── test_rules.py
    ├── test_risk.py
    └── test_pipeline.py
```

## Requirements

- Python 3.10+
- 4 GB RAM recommended
- No real network interface required

## Installation

### Windows PowerShell

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Linux/macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run the complete pipeline

Generate 1,000 synthetic flow records:

```bash
python scripts/generate_data.py --rows 1000 --output data/raw/network_flows.csv
```

Run IDS detection:

```bash
python scripts/run_detection.py --input data/raw/network_flows.csv
```

Generate an incident report:

```bash
python scripts/generate_report.py
```

Launch the dashboard:

```bash
streamlit run app.py
```

Then open the local URL printed by Streamlit.

## What the synthetic records represent

The generator creates harmless records such as:

- Normal web traffic
- Normal DNS traffic
- Normal SSH administration
- High-volume connection patterns
- Repeated failed-connection patterns
- Unusual port activity
- ICMP-heavy patterns
- Large byte-transfer anomalies
- Connection-rate anomalies

These are **records**, not real attacks. No packets are sent to other systems.

## Detection logic

### Rule/signature layer

Examples:

1. Very high connection rate from one source
2. Repeated failed connections
3. Unusual destination port
4. Excessive ICMP activity
5. Abnormally high bytes transferred

Each rule contributes a weighted risk score.

### Anomaly layer

The anomaly detector learns normal statistical ranges from the synthetic flow dataset and flags outliers using robust z-score style measurements.

### ML layer

If enabled, `IsolationForest` is trained on generated flow features. It is used as an additional signal rather than the only decision-maker.

## Risk model

A simplified score is calculated from:

```text
Risk =
    Rule score
  + Anomaly contribution
  + ML contribution
```

The score is capped at 100.

Suggested severity:

```text
0–19    INFO
20–39   LOW
40–59   MEDIUM
60–79   HIGH
80–100  CRITICAL
```

## SOC investigation workflow

The dashboard supports:

1. View overall traffic
2. Filter alerts by severity/classification
3. Inspect source/destination information
4. Review triggered rules
5. Review anomaly evidence
6. Review risk score
7. Export incident data
8. Generate an incident report

## Testing

Run:

```bash
pytest -q
```

## Docker

```bash
docker compose up --build
```

The dashboard is then available locally on port 8501.

## GitHub strategy

Suggested repository name:

`network-intrusion-detection-system`

Recommended commits:

1. `Initial project structure`
2. `Add synthetic traffic generator`
3. `Add signature based detection`
4. `Add anomaly detection`
5. `Add optional ML detector`
6. `Add SQLite alert storage`
7. `Add Streamlit SOC dashboard`
8. `Add reports and tests`
9. `Add Docker support`
10. `Improve README and documentation`

Do not upload:

- `.venv/`
- `__pycache__/`
- SQLite runtime database
- private credentials
- real PCAPs
- real organizational traffic

## LinkedIn project description

**Network Intrusion Detection System (IDS) Simulation**

Built a defensive IDS simulation that generates synthetic network-flow data and detects suspicious behavior using rule-based signatures, statistical anomaly detection, and an optional Isolation Forest model. Implemented risk scoring, severity classification, SQLite event storage, SOC-style investigation views, incident reporting, automated tests, and a Streamlit security dashboard. Designed entirely for safe offline cybersecurity experimentation.

## Resume bullets

- Built a Python-based Network Intrusion Detection System using synthetic network-flow records, signature/rule-based detection, anomaly analysis, and optional Isolation Forest ML.
- Implemented risk scoring, severity classification, SQLite security-event storage, incident reporting, and a Streamlit SOC-style monitoring dashboard.
- Added automated testing and Docker support while keeping all attack-like activity isolated to synthetic/local simulation.

## Important academic note

This project is an IDS **simulation**. It demonstrates defensive detection engineering without claiming that it performs real enterprise packet inspection. A future extension could ingest authorized NetFlow/Zeek records from a controlled lab.
