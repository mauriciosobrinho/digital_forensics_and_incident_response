from datetime import datetime, timezone
from typing import Any


def _parse_datetime(value: str | None) -> datetime | None:
    if not value:
        return None

    parsed: datetime | None = None

    try:
        parsed = datetime.fromisoformat(
            str(value).replace("Z", "+00:00")
        )
    except ValueError:
        try:
            parsed = datetime.strptime(
                str(value),
                "%Y-%m-%d %H:%M:%S.%f",
            )
        except ValueError:
            try:
                parsed = datetime.strptime(
                    str(value),
                    "%Y-%m-%d %H:%M:%S",
                )
            except ValueError:
                return None

    if parsed.tzinfo is None:
        parsed = parsed.replace(
            tzinfo=timezone.utc,
        )

    return parsed


def _hours_between(
    start: datetime | None,
    end: datetime | None,
) -> float | None:
    if not start or not end:
        return None

    seconds = max(
        0.0,
        (end - start).total_seconds(),
    )

    return round(
        seconds / 3600,
        4,
    )


def build_response_metrics(
    *,
    forensic_evidence: dict[str, Any],
    agent_investigation: dict[str, Any],
) -> dict[str, Any]:

    generated_at = datetime.now(
        timezone.utc
    )

    timeline_summary = (
        forensic_evidence
        .get("attack_timeline", {})
        .get("summary", {})
    )

    if not timeline_summary:
        timeline_summary = (
            forensic_evidence
            .get("summary", {})
        )

    attack_window = (
        agent_investigation
        .get("forensic_analysis", {})
        .get("attack_window", {})
    )

    first_seen = (
        attack_window.get("first_seen")
        or timeline_summary.get("first_seen")
    )

    last_seen = (
        attack_window.get("last_seen")
        or timeline_summary.get("last_seen")
    )

    first_seen_dt = _parse_datetime(first_seen)
    last_seen_dt = _parse_datetime(last_seen)

    response_time = _parse_datetime(
        agent_investigation
        .get("response_recommendation", {})
        .get("generated_at_utc")
    ) or generated_at

    containment_time = _parse_datetime(
        agent_investigation
        .get("human_approval_response", {})
        .get("generated_at_utc")
    ) or generated_at

    detection_candidates = [
        response_time,
        containment_time,
        generated_at,
    ]

    detection_time = min(
        candidate
        for candidate in detection_candidates
        if candidate is not None
    )

    ttd_hours = _hours_between(
        first_seen_dt,
        detection_time,
    )

    ttr_hours = _hours_between(
        detection_time,
        response_time,
    )

    ttc_hours = _hours_between(
        detection_time,
        containment_time,
    )

    return {
        "metrics_type": "nist_incident_response_metrics",
        "generated_at_utc": generated_at.isoformat(),
        "attack_window": {
            "first_seen": first_seen,
            "last_seen": last_seen,
        },
        "time_to_detect": {
            "metric": "TTD",
            "definition": (
                "Time between first observed malicious activity "
                "and platform detection."
            ),
            "value_hours": ttd_hours,
            "interpretation": (
                "Computed from first_seen to current detection execution time. "
                "For this historical dataset, the value reflects retrospective "
                "detection latency."
            ),
        },
        "time_to_respond": {
            "metric": "TTR",
            "definition": (
                "Time between detection and response recommendation generation."
            ),
            "value_hours": ttr_hours,
            "interpretation": (
                "In the automated pipeline, response recommendation is generated "
                "during the same execution cycle."
            ),
        },
        "time_to_contain": {
            "metric": "TTC",
            "definition": (
                "Time between detection and containment approval or simulated "
                "containment decision."
            ),
            "value_hours": ttc_hours,
            "interpretation": (
                "Because the platform runs in dry-run mode, TTC represents time "
                "to simulated containment approval, not production containment."
            ),
        },
        "automation_impact": {
            "manual_process_baseline": (
                "Manual DFIR triage and evidence review may take hours or days "
                "depending on analyst availability and data volume."
            ),
            "automated_process_observed": (
                "The platform generates detection, forensic evidence, response "
                "recommendations and approval artifacts in a single pipeline run."
            ),
            "expected_reduction": (
                "Automation reduces TTD/TTR/TTC by consolidating evidence extraction, "
                "risk scoring, anomaly detection, agent reasoning and playbook "
                "generation."
            ),
        },
    }