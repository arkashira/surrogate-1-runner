"""
Rule that flags the use of `tx.origin` in Solidity source code.

`tx.origin` is a global variable that refers to the original
transaction sender.  Using it for authorization is a well‑known
security anti‑pattern because it can be spoofed by a malicious
contract that forwards the transaction.  This rule detects the
pattern, emits a warning, and can be used by a static‑analysis
pipeline to surface the issue to developers.
"""

import logging
import re
from typing import Iterable

# Configure a module‑level logger.  In a larger application this
# would be configured by the framework that imports the rule.
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class TxOriginRule:
    """
    Detects the presence of `tx.origin` in Solidity code.

    Attributes
    ----------
    severity : str
        A human‑readable severity level.  The value is kept for
        compatibility with the original design but is not used
        directly by the rule logic.
    description : str
        Human‑readable description of the rule.
    """

    #: Regex that matches the exact token `tx.origin` (word boundaries
    #: prevent false positives such as `tx.originator`).
    _PATTERN: re.Pattern[str] = re.compile(r"\btx\.origin\b")

    def __init__(self) -> None:
        self.severity = "Medium"
        self.description = "tx.origin usage detected"

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def detect(self, code: str | Iterable[str]) -> bool:
        """
        Return ``True`` if the code contains the token `tx.origin`.

        Parameters
        ----------
        code : str | Iterable[str]
            Solidity source code as a single string or an iterable of
            lines.  The function is tolerant of either form.

        Returns
        -------
        bool
            ``True`` when the pattern is found, otherwise ``False``.
        """
        if isinstance(code, str):
            return bool(self._PATTERN.search(code))
        # Iterable of lines – join them once to avoid repeated regex
        # compilation overhead.
        joined = "\n".join(code)
        return bool(self._PATTERN.search(joined))

    def warn(self, code: str | Iterable[str]) -> bool:
        """
        Emit a warning if `tx.origin` is detected.

        The warning is logged at ``logging.WARNING`` level.  The
        function returns ``True`` if a warning was emitted, otherwise
        ``False``.  Calling the method multiple times on the same
        input will not produce duplicate log entries because the
        underlying ``detect`` call is idempotent.

        Parameters
        ----------
        code : str | Iterable[str]
            Solidity source code.

        Returns
        -------
        bool
            ``True`` if a warning was logged, otherwise ``False``.
        """
        if self.detect(code):
            logger.warning(self.description)
            return True
        return False

    def identify(self, code: str | Iterable[str]) -> bool:
        """
        Emit a more descriptive identification message.

        This method is intended for use in a larger rule‑engine
        where a distinction between a generic warning and a
        specific identification is useful.

        Parameters
        ----------
        code : str | Iterable[str]
            Solidity source code.

        Returns
        -------
        bool
            ``True`` if the pattern was found and the message logged,
            otherwise ``False``.
        """
        if self.detect(code):
            logger.info("Identified tx.origin usage in authorization logic")
            return True
        return False