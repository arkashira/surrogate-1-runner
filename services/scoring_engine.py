import math

class ScoringEngine:
    SEVERITY_WEIGHTS = {
        'critical': 100,
        'high': 70,
        'medium': 40,
        'low': 20
    }

    @staticmethod
    def calculate_audit_score(policy_severity: str, code_change_frequency: int) -> int:
        """
        Calculate audit impact score based on policy severity and code change frequency
        Score = (policy_severity * 0.6) + (code_change_frequency * 0.4)
        Returns integer value between 1-100
        """
        severity_value = ScoringEngine.SEVERITY_WEIGHTS.get(policy_severity, 20)
        raw_score = (severity_value * 0.6) + (code_change_frequency * 0.4)
        return max(1, min(100, round(raw_score)))