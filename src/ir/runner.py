import json
from pathlib import Path
from typing import Any

from src.config.settings import (
    AGENT_INVESTIGATION_FILE,
    CONTAINMENT_STRATEGY_FILE,
    FORENSIC_EVIDENCE_FILE,
    NIST_INCIDENT_REPORT_FILE,
    RESPONSE_METRICS_FILE,
    ROOT_CAUSE_ANALYSIS_FILE,
)
from src.ir.containment_strategy import (
    build_containment_strategy,
)
from src.ir.nist_lifecycle import (
    build_nist_incident_report,
)
from src.ir.response_metrics import (
    build_response_metrics,
)
from src.ir.root_cause_analysis import (
    build_root_cause_analysis,
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(
        "r",
        encoding="utf-8",
    ) as f:
        return json.load(f)


def _save_json(
    data: dict[str, Any],
    path: Path,
) -> None:
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with path.open(
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(
            data,
            f,
            indent=2,
            ensure_ascii=False,
            default=str,
        )


def run_nist_incident_response() -> dict[str, Any]:
    forensic_evidence = _load_json(
        FORENSIC_EVIDENCE_FILE
    )

    agent_investigation = _load_json(
        AGENT_INVESTIGATION_FILE
    )

    response_metrics = build_response_metrics(
        forensic_evidence=forensic_evidence,
        agent_investigation=agent_investigation,
    )

    containment_strategy = build_containment_strategy(
        forensic_evidence=forensic_evidence,
        agent_investigation=agent_investigation,
    )

    root_cause_analysis = build_root_cause_analysis(
        forensic_evidence=forensic_evidence,
        agent_investigation=agent_investigation,
    )

    nist_report = build_nist_incident_report(
        forensic_evidence=forensic_evidence,
        agent_investigation=agent_investigation,
        response_metrics=response_metrics,
        containment_strategy=containment_strategy,
        root_cause_analysis=root_cause_analysis,
    )

    _save_json(
        response_metrics,
        RESPONSE_METRICS_FILE,
    )

    _save_json(
        containment_strategy,
        CONTAINMENT_STRATEGY_FILE,
    )

    _save_json(
        root_cause_analysis,
        ROOT_CAUSE_ANALYSIS_FILE,
    )

    _save_json(
        nist_report,
        NIST_INCIDENT_REPORT_FILE,
    )

    return nist_report


def main() -> None:
    report = run_nist_incident_response()

    summary = report["incident_summary"]

    print("\nNIST Incident Response report generated.")
    print(
        f"Severity: {summary.get('severity')} | "
        f"Priority: {summary.get('priority')} | "
        f"Dry-run: {summary.get('dry_run')}"
    )


if __name__ == "__main__":
    main()