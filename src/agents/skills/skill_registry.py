from typing import Any

from src.agents.skills.containment_skill import run_containment_skill
from src.agents.skills.impact_skill import run_impact_skill
from src.agents.skills.metrics_skill import run_metrics_skill
from src.agents.skills.mitre_skill import run_mitre_skill
from src.agents.skills.patient_zero_skill import run_patient_zero_skill
from src.agents.skills.root_cause_skill import run_root_cause_skill
from src.agents.skills.timeline_skill import run_timeline_skill


def run_all_skills(
    artifacts: dict[str, Any],
) -> dict[str, Any]:
    return {
        "patient_zero": run_patient_zero_skill(artifacts),
        "timeline": run_timeline_skill(artifacts),
        "containment": run_containment_skill(artifacts),
        "impact": run_impact_skill(artifacts),
        "mitre": run_mitre_skill(artifacts),
        "root_cause": run_root_cause_skill(artifacts),
        "metrics": run_metrics_skill(artifacts),
    }