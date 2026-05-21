"""
LLM Pattern implementation for surrogate-1.

This module defines the LLMPattern class which orchestrates
LLM calls, rule enforcement, and audit logging.  It is
designed to be plug‑in‑ready for any LLM client that
exposes a ``call(prompt: str) -> str`` interface.
"""

import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Optional

# Configure module‑level logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(
    logging.Formatter("[%(asctime)s] %(levelname)s %(name)s: %(message)s")
)
logger.addHandler(handler)


class LLMPattern:
    """
    Orchestrates LLM interactions, rule enforcement, and audit logging.

    Parameters
    ----------
    llm_client : Any
        An object with a ``call(prompt: str) -> str`` method.
    policy : Callable[[str], bool]
        A function that receives the LLM's raw output and returns
        ``True`` if the decision is acceptable, ``False`` otherwise.
    audit_log_path : str | Path
        Path to a JSONL file where audit records are appended.
    """

    def __init__(
        self,
        llm_client: Any,
        policy: Callable[[str], bool],
        audit_log_path: str | Path,
    ) -> None:
        self.llm_client = llm_client
        self.policy = policy
        self.audit_log_path = Path(audit_log_path)
        # Ensure audit log directory exists
        self.audit_log_path.parent.mkdir(parents=True, exist_ok=True)

    def run(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Execute the LLM pattern.

        Parameters
        ----------
        prompt : str
            The prompt to send to the LLM.
        context : dict, optional
            Additional context that may be useful for the audit trail.

        Returns
        -------
        dict
            Structured result containing:
                - decision: str
                - rationale: str
                - timestamp: str (ISO 8601)
                - context: dict (original context)
        """
        logger.info("Sending prompt to LLM")
        raw_output = self.llm_client.call(prompt)

        # Simple split: first line is decision, rest is rationale
        lines = raw_output.strip().splitlines()
        decision = lines[0] if lines else ""
        rationale = "\n".join(lines[1:]) if len(lines) > 1 else ""

        # Enforce policy
        is_acceptable = self.policy(decision)
        if not is_acceptable:
            logger.warning("Policy violation detected. Decision rejected.")
            decision = "REJECTED"
            rationale = "Policy violation: decision not allowed."

        record = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "prompt": prompt,
            "decision": decision,
            "rationale": rationale,
            "context": context or {},
        }

        self._audit(record)
        return record

    def _audit(self, record: Dict[str, Any]) -> None:
        """
        Append the audit record to the JSONL audit log.

        Parameters
        ----------
        record : dict
            The audit record to write.
        """
        try:
            with self.audit_log_path.open("a", encoding="utf-8") as fh:
                fh.write(json.dumps(record) + "\n")
            logger.debug(f"Audit record written to {self.audit_log_path}")
        except Exception as exc:
            logger.error(f"Failed to write audit record: {exc}")

    @staticmethod
    def default_policy(decision: str) -> bool:
        """
        Default policy that rejects decisions containing prohibited words.

        Parameters
        ----------
        decision : str
            The decision string from the LLM.

        Returns
        -------
        bool
            ``True`` if decision is acceptable, ``False`` otherwise.
        """
        prohibited = {"reject", "disallow", "no", "deny"}
        # Case‑insensitive check
        return not any(word.lower() in decision.lower() for word in prohibited)


# Example usage (would be removed in production code)
if __name__ == "__main__":
    class DummyLLM:
        def call(self, prompt: str) -> str:
            return "APPROVE\nThe request meets all criteria."

    pattern = LLMPattern(
        llm_client=DummyLLM(),
        policy=LLMPattern.default_policy,
        audit_log_path="audit.log",
    )
    result = pattern.run("Should we approve this request?", {"user_id": 42})
    print(result)