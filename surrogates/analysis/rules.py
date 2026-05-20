from surrogates.analysis.access_control_rule import UnrestrictedPublicFunctionRule
from surrogates.analysis.base import LintRule

def get_rules(config: dict) -> t.List[LintRule]:
    """Return list of all applicable lint rules."""
    return [
        UnrestrictedPublicFunctionRule(config),
        # Add other rules here if needed
    ]