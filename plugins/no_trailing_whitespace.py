from typing import Iterable
from surrogate_1.types import ScanContext, Detection

DEFAULT_SEVERITY = "LOW"

def detect(context: ScanContext) -> Iterable[Detection]:
    """
    Detect lines that end with trailing whitespace.
    """
    for idx, line in enumerate(context.content.splitlines(), start=1):
        if line.rstrip() != line:
            yield Detection(
                rule_id="no_trailing_whitespace",
                severity=DEFAULT_SEVERITY,
                message="Trailing whitespace detected",
                location=f"{context.file_path}:{idx}"
            )