# SOC Copilot Sample Output

## Who is the patient zero candidate?

The patient zero candidate is identified by correlating the earliest exploitation window, high-risk source IP behavior, invoice diversity and risk scoring signals.

## Was the attack automated?

Yes. The behavior is compatible with automated invoice enumeration: high request volume, high unique invoice diversity, sequential object access, bot-detection convergence and anomaly-detection convergence.

## Which containment actions are recommended?

Dynamic rate limiting, intensified monitoring, selective IP challenge/blocking with human approval, suspicious token review and WAF rule updates.

## Why is human approval required?

Human approval is required because containment can create false positives and business impact. The platform operates in dry-run mode and requires analyst governance for risky actions.

## What happens if more evidence is requested?

The LangGraph workflow re-enters forensic analysis, generates additional reasoning and returns to response advice and human approval.
