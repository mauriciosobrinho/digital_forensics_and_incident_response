from dataclasses import dataclass, asdict


@dataclass(frozen=True)
class EnterpriseSliSlo:
    sli_detection_success_rate: float = 0.97
    sli_evidence_completeness: float = 0.95
    sli_containment_readiness: float = 1.0
    slo_detection_target: float = 0.95
    slo_response_target: float = 0.90
    slo_containment_target: float = 0.90

    def to_dict(self) -> dict:
        return asdict(self)


def build_sli_slo_registry() -> dict:
    return EnterpriseSliSlo().to_dict()