# Interview Preparation

## 1. What is an IDS?

An Intrusion Detection System monitors activity and identifies events that may indicate malicious or policy-violating behavior. It generally produces alerts rather than automatically blocking traffic.

## 2. Why did you use synthetic traffic?

The project is designed as a safe academic simulation. Synthetic records allow detection engineering without generating malicious traffic against real systems.

## 3. Signature vs anomaly detection

Signature detection looks for known patterns or thresholds. It is explainable and useful for known behaviors.

Anomaly detection learns what is normal and identifies deviations. It can discover previously unseen patterns but may create false positives.

## 4. Why combine both?

Rules provide explainability. Anomaly and ML scores provide additional evidence. Combining them gives a more useful risk-prioritization approach.

## 5. Why Isolation Forest?

Isolation Forest is an unsupervised algorithm designed to isolate unusual observations. It is suitable for demonstrating anomaly detection when labeled attack data is limited.

## 6. What features are used?

Duration, packets, bytes sent/received, failed connections, connection rate, source port and destination port.

## 7. What is a false positive?

A false positive occurs when legitimate activity is incorrectly flagged as suspicious.

## 8. What is a false negative?

A false negative occurs when suspicious activity is missed by the detector.

## 9. What does a SOC analyst do with an alert?

Validate the alert, inspect source/destination context, review triggered evidence, correlate related events, determine severity, document findings and escalate according to procedure.

## 10. Is this a real enterprise IDS?

No. It is an IDS simulation and detection-engineering project. It demonstrates the architecture and concepts without claiming production packet-level visibility.

## 11. How would you improve it?

I would add authorized Zeek/NetFlow ingestion, alert correlation, MITRE ATT&CK tagging, centralized logging, model evaluation, role-based access and SIEM integration.

## 12. How did you keep it safe?

No public scanning, exploitation, attack traffic or third-party monitoring is used. Attack-like conditions exist only as generated flow records.
