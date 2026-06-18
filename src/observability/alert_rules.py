class AlertRuleRegistry:
    def list_rules(self) -> list[dict]:
        return [
            {
                "alert": "DFIRPlatformDown",
                "expr": "dfir_platform_health == 0",
                "severity": "critical",
                "description": "DFIR platform health metric indicates degraded state.",
            },
            {
                "alert": "HighIDORFindings",
                "expr": "dfir_idor_findings > 100",
                "severity": "warning",
                "description": "High volume of IDOR findings detected.",
            },
            {
                "alert": "LowEvaluationScore",
                "expr": "dfir_evaluation_score < 0.80",
                "severity": "warning",
                "description": "Agent evaluation score is below acceptable threshold.",
            },
        ]