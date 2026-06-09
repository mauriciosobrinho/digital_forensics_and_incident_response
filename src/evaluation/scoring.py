from typing import Any


def _contains_key_deep(
    payload: Any,
    key: str,
) -> bool:
    if isinstance(payload, dict):
        if key in payload:
            return True

        return any(
            _contains_key_deep(value, key)
            for value in payload.values()
        )

    if isinstance(payload, list):
        return any(
            _contains_key_deep(item, key)
            for item in payload
        )

    if isinstance(payload, str):
        return key.lower() in payload.lower()

    return False


def score_requirement(
    payload: dict[str, Any],
    required_evidence: list[str],
) -> dict[str, Any]:
    checks = []

    for evidence_key in required_evidence:
        found = _contains_key_deep(
            payload,
            evidence_key,
        )

        checks.append(
            {
                "evidence": evidence_key,
                "found": found,
            }
        )

    total = len(checks)
    passed = sum(
        1
        for check in checks
        if check["found"]
    )

    score = (
        round(
            passed / total,
            4,
        )
        if total
        else 0.0
    )

    return {
        "score": score,
        "passed_checks": passed,
        "total_checks": total,
        "checks": checks,
        "status": (
            "passed"
            if score == 1.0
            else "partial"
            if score > 0
            else "failed"
        ),
    }