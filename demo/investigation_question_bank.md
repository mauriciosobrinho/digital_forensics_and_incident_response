# Investigation Question Bank

This guide is designed for reviewers who are not specialized in cyber forensics. It demonstrates how the platform supports incident investigation, impact assessment, containment planning and SOC monitoring.

## Detection

1. How does the platform detect IDOR-like behavior?
2. Which features support the classification?
3. What is the difference between an IDOR finding and an anomaly?
4. Why is invoice diversity relevant?
5. How does risk scoring prioritize investigation?

## Forensics

1. Who is the patient zero candidate?
2. When did the exploitation start?
3. When did the exploitation end?
4. Which invoices were involved?
5. Which IOCs were generated?
6. Which MITRE ATT&CK concepts apply?

## Impact

1. How many attack events were observed?
2. How many tokens appeared in suspicious activity?
3. What is the operational impact?
4. What is the potential regulatory risk?

## Automation

1. Was the attack automated?
2. Which signals indicate automation?
3. Is there convergence between bot detection and anomaly detection?

## Containment and Eradication

1. Which immediate containment actions are recommended?
2. Which actions require human approval?
3. Why can rate limiting be safer than immediate blocking?
4. What root cause must be fixed permanently?

## Human Approval

1. What happens if the reviewer approves?
2. What happens if the reviewer rejects?
3. What happens if the reviewer modifies the plan?
4. What happens if more evidence is requested?

## NIST Metrics

1. What is TTD?
2. What is TTR?
3. What is TTC?
4. Why is TTD retrospective in this dataset?

## Observability

1. How do we know the platform worked?
2. What is the platform health status?
3. Which SOC metrics are monitored?
