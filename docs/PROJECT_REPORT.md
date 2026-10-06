# Network Intrusion Detection System (IDS) Simulation — Project Report

## 1. Introduction

A Network Intrusion Detection System monitors network activity and identifies behavior that may indicate security threats. This project implements an educational IDS simulation using synthetic network-flow records.

The system combines explainable rules with statistical anomaly detection and an optional machine-learning detector. Results are assigned a risk score and severity and are stored for SOC-style investigation.

## 2. Problem Statement

Traditional manual inspection of network-flow records is difficult when traffic volume becomes large. Security analysts need automated mechanisms to identify unusual behavior, prioritize alerts, and investigate the evidence behind each alert.

## 3. Objectives

- Generate safe synthetic network traffic records.
- Extract useful network-flow features.
- Detect known suspicious patterns using signatures/rules.
- Identify statistical outliers.
- Demonstrate optional ML-based anomaly detection.
- Calculate risk scores.
- Classify events and assign severity.
- Store alerts in a database.
- Provide a SOC-style dashboard.
- Generate incident reports.

## 4. Scope

The project is intentionally a simulation. It does not perform network scanning, exploitation, packet flooding, credential attacks, or unauthorized monitoring.

## 5. System Modules

### 5.1 Synthetic Traffic Generator

Creates flow records containing source/destination IPs, protocol, ports, duration, packets, bytes, failed connections and connection rate.

### 5.2 Rule Engine

Uses transparent thresholds to detect suspicious patterns.

### 5.3 Anomaly Detector

Computes robust statistical outlier scores across traffic features.

### 5.4 ML Detector

Isolation Forest provides an optional unsupervised anomaly signal.

### 5.5 Risk Engine

Combines multiple signals into a score from 0 to 100.

### 5.6 Alert Engine

Maps risk scores to severity and classification.

### 5.7 Database

SQLite stores alert records for later investigation.

### 5.8 Dashboard

Streamlit displays metrics, charts, filters and alert details.

### 5.9 Reporting

Creates a Markdown incident report summarizing high-risk events.

## 6. Technologies

- Python
- Pandas
- NumPy
- Scikit-learn
- SQLite
- Streamlit
- Plotly
- Pytest
- Docker
- Git/GitHub

## 7. Detection Methodology

The system first evaluates deterministic rules. It then calculates statistical anomaly scores and, when enabled, an Isolation Forest score.

The risk score is:

`0.55 × rule score + 0.30 × anomaly score + 0.15 × ML score`

A small additional correlation bonus is used when multiple rules trigger.

## 8. Severity

| Risk | Severity |
|---:|---|
| 0–19 | INFO |
| 20–39 | LOW |
| 40–59 | MEDIUM |
| 60–79 | HIGH |
| 80–100 | CRITICAL |

## 9. Security and Ethics

All attack-like scenarios are synthetic. Documentation uses reserved/test-style IP ranges and generated records. The project must only be extended with real telemetry when the student has explicit authorization.

## 10. Future Enhancements

- Authorized Zeek/NetFlow ingestion
- PCAP analysis in an isolated lab
- Alert deduplication
- MITRE ATT&CK mapping
- GeoIP enrichment using approved data
- Role-based analyst accounts
- Elasticsearch/OpenSearch integration
- Kafka streaming
- SIEM integration
- Model monitoring and drift detection
