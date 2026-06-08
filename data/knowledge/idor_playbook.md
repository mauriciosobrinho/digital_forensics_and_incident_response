# IDOR Investigation Playbook

IDOR occurs when an application exposes a direct object reference and fails to verify whether the requester is authorized to access that object.

Relevant signals:
- High unique object diversity per client
- Sequential object ID access
- High success rate across unrelated object IDs
- Repeated access to invoice-like identifiers
- Automation patterns such as stable user-agent and high request volume

Investigation steps:
1. Identify high-risk IPs.
2. Confirm invoice diversity.
3. Inspect sequential_access_ratio.
4. Compare with anomaly detection.
5. Review tokens and user-agents.
6. Recommend containment in dry-run first.