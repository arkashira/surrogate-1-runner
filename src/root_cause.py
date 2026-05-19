import yaml
from typing import List, Tuple
from .model import DiagnosticOutput

# ----------------------------------------------------------------------
# Default rule‑set (can be overridden by a YAML file at runtime)
# ----------------------------------------------------------------------
_DEFAULT_RULES = """
- when: "resource_usage"
  contains: "high memory"
  cause: "High memory usage"
- when: "logs"
  contains: "error"
  cause: "Application error"
- when: "config_diff"
  contains: "misconfiguration"
  cause: "Configuration issue"
"""

def _load_rules(path: str | None = None) -> List[dict]:
    if path:
        with open(path, "r") as f:
            return yaml.safe_load(f)
    return yaml.safe_load(_DEFAULT_RULES)


def infer_root_cause(diag: DiagnosticOutput, rule_file: str | None = None) -> str:
    """
    Walk the rule list in order; first match wins.
    Returns a human‑readable cause or “Unknown root cause”.
    """
    rules = _load_rules(rule_file)

    for rule in rules:
        field_val: str | None = getattr(diag, rule["when"])
        if field_val and rule["contains"].lower() in field_val.lower():
            return rule["cause"]
    return "Unknown root cause"