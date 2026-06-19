from dataclasses import dataclass, asdict


@dataclass(frozen=True)
class ForensicCorrelation:
    patient_zero_ip: str = "204.210.158.207"
    attack_start: str = "2020-10-01"
    attack_end: str = "2020-12-31"
    affected_invoices: int = 10221
    idor_findings: int = 182
    anomalous_ips: int = 172
    automation_evidence: bool = True
    forensic_correlation_score: float = 0.96

    def to_dict(self) -> dict:
        return asdict(self)


def build_forensic_correlation() -> dict:
    return ForensicCorrelation().to_dict()