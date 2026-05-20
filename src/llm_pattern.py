import json
import os
import time
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional


class LLMRuleError(Exception):
    """Raised when LLM output violates a defined rule."""
    pass


class LLMPattern:
    """
    Prototype for integrating an LLM‑based judgment into a workflow.

    Features
    --------
    * Deterministic mock LLM (can be overridden with a custom callable).
    * Rule enforcement – each rule is a callable that receives the LLM output
      and must return ``True`` to pass.
    * Audit trail – every invocation is logged as a JSON line to the supplied
      ``audit_path``.
    """

    def __init__(
        self,
        *,
        audit_path: str,
        rules: Optional[List[Callable[[str], bool]]] = None,
        llm_callable: Optional[Callable[[Dict[str, Any]], str]] = None,
    ) -> None:
        """
        Parameters
        ----------
        audit_path: str
            File path where audit entries are appended (JSON‑lines format).
        rules: list of callables, optional
            Functions that accept the LLM output string and return ``True`` if
            the output satisfies the rule.
        llm_callable: callable, optional
            Function that receives the input payload and returns the LLM decision.
            If omitted a simple deterministic mock implementation is used.
        """
        self.audit_path = audit_path
        os.makedirs(os.path.dirname(self.audit_path), exist_ok=True)

        self.rules = rules or [self._default_approval_rule]
        self.llm_callable = llm_callable or self._default_mock_llm

    @staticmethod
    def _default_approval_rule(output: str) -> bool:
        """Rule: output must be either 'APPROVE' or 'REJECT'."""
        return output in {"APPROVE", "REJECT"}

    @staticmethod
    def _default_mock_llm(payload: Dict[str, Any]) -> str:
        """
        Very simple deterministic mock LLM.

        Returns ``APPROVE`` when ``payload['value']`` >= 10, otherwise ``REJECT``.
        """
        value = payload.get("value", 0)
        return "APPROVE" if value >= 10 else "REJECT"

    def _enforce_rules(self, output: str) -> None:
        """Validate the LLM output against all configured rules."""
        for rule in self.rules:
            if not rule(output):
                raise LLMRuleError(f"LLM output '{output}' violated a rule.")

    def _write_audit_entry(
        self,
        payload: Dict[str, Any],
        output: str,
        rule_passed: bool,
        duration_ms: float,
    ) -> None:
        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "payload": payload,
            "llm_output": output,
            "rule_passed": rule_passed,
            "duration_ms": duration_ms,
        }
        line = json.dumps(entry, ensure_ascii=False)
        with open(self.audit_path, "a", encoding="utf-8") as f:
            f.write(line + "\n")

    def evaluate(self, payload: Dict[str, Any]) -> str:
        """
        Run the LLM on ``payload``, enforce rules, and record an audit entry.

        Returns
        -------
        str
            The LLM decision (e.g., ``'APPROVE'`` or ``'REJECT'``).

        Raises
        ------
        LLMRuleError
            If any rule is violated.
        """
        start = time.time()
        output = self.llm_callable(payload)
        try:
            self._enforce_rules(output)
            rule_passed = True
        except LLMRuleError:
            rule_passed = False
            raise
        finally:
            duration_ms = (time.time() - start) * 1000.0
            self._write_audit_entry(payload, output, rule_passed, duration_ms)
        return output

    # --------------------------------------------------------------------- #
    # Helper for sample workflow integration
    # --------------------------------------------------------------------- #
    def process_workflow_item(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """
        Example integration point for a workflow step.

        The method evaluates the LLM decision and annotates the item with the
        result under the ``'llm_decision'`` key.

        Parameters
        ----------
        item: dict
            Arbitrary workflow payload.

        Returns
        -------
        dict
            The original payload enriched with ``'llm_decision'``.
        """
        decision = self.evaluate(item)
        enriched = dict(item)  # shallow copy to avoid side‑effects
        enriched["llm_decision"] = decision
        return enriched