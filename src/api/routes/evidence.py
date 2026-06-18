import json
from pathlib import Path

from fastapi import APIRouter

from src.config.settings import (
    ATTACK_TIMELINE_FILE,
    FORENSIC_EVIDENCE_FILE,
    IOCS_FILE,
    NIST_INCIDENT_REPORT_FILE,
)


router = APIRouter(
    prefix="/api",
    tags=["evidence"],
)


def _exists(path: Path) -> bool:
    return path.exists()


def _load_json(path: Path) -> dict | list | None:
    if not path.exists():
        return None

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


@router.get("/evidence")
def get_evidence() -> dict:
    forensic_evidence = _load_json(FORENSIC_EVIDENCE_FILE)
    nist_report = _load_json(NIST_INCIDENT_REPORT_FILE)

    evidence_summary = (
        forensic_evidence.get("summary", {})
        if isinstance(forensic_evidence, dict)
        else {}
    )

    incident_summary = (
        nist_report.get("incident_summary", {})
        if isinstance(nist_report, dict)
        else {}
    )

    return {
        "service": "dfir-evidence",
        "available": {
            "forensic_evidence": _exists(FORENSIC_EVIDENCE_FILE),
            "attack_timeline": _exists(ATTACK_TIMELINE_FILE),
            "iocs": _exists(IOCS_FILE),
            "nist_incident_report": _exists(NIST_INCIDENT_REPORT_FILE),
        },
        "summary": evidence_summary,
        "incident_summary": incident_summary,
        "source_files": {
            "forensic_evidence": str(FORENSIC_EVIDENCE_FILE),
            "attack_timeline": str(ATTACK_TIMELINE_FILE),
            "iocs": str(IOCS_FILE),
            "nist_incident_report": str(NIST_INCIDENT_REPORT_FILE),
        },
    }