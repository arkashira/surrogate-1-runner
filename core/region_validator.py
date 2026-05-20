import json
import threading
from pathlib import Path
from typing import Set, Iterable

class RegionPolicyError(Exception):
    """Raised when the region policy file is missing or malformed."""
    pass

class RegionValidator:
    """
    Validates whether a given region is permitted to access AI tools.

    The validator loads a JSON policy file that contains an ``allowed_regions``
    array.  The file is watched for changes and reloaded lazily in a thread‑safe
    manner.

    Example policy file (``schemas/region_policy.json``)::

        {
            "allowed_regions": ["us-east-1", "eu-west-1"]
        }
    """

    _instance_lock = threading.Lock()
    _instance = None

    @classmethod
    def get_instance(cls, policy_path: Path | str = None) -> "RegionValidator":
        """
        Singleton accessor.  If ``policy_path`` is omitted the default location
        ``/opt/axentx/surrogate-1/schemas/region_policy.json`` is used.
        """
        with cls._instance_lock:
            if cls._instance is None:
                cls._instance = cls(policy_path)
            return cls._instance

    def __init__(self, policy_path: Path | str = None):
        self.policy_path = Path(
            policy_path or "/opt/axentx/surrogate-1/schemas/region_policy.json"
        )
        self._allowed_regions: Set[str] = set()
        self._policy_mtime: float = 0.0
        self._load_policy()

    def _load_policy(self) -> None:
        """Load the JSON policy file and cache the allowed regions."""
        if not self.policy_path.is_file():
            raise RegionPolicyError(f"Region policy file not found: {self.policy_path}")

        try:
            with self.policy_path.open("r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError as exc:
            raise RegionPolicyError(f"Invalid JSON in region policy: {exc}") from exc

        allowed = data.get("allowed_regions")
        if not isinstance(allowed, list) or not all(isinstance(r, str) for r in allowed):
            raise RegionPolicyError(
                "Region policy must contain an 'allowed_regions' list of strings."
            )

        self._allowed_regions = {r.strip().lower() for r in allowed if r.strip()}
        self._policy_mtime = self.policy_path.stat().st_mtime

    def _maybe_reload(self) -> None:
        """Reload the policy if the file has changed since the last load."""
        try:
            current_mtime = self.policy_path.stat().st_mtime
        except FileNotFoundError:
            raise RegionPolicyError(f"Region policy file disappeared: {self.policy_path}")

        if current_mtime != self._policy_mtime:
            self._load_policy()

    def is_allowed(self, region: str) -> bool:
        """
        Return ``True`` if ``region`` is in the allowed list, ``False`` otherwise.

        The check is case‑insensitive and whitespace‑agnostic.
        """
        if not isinstance(region, str):
            return False

        self._maybe_reload()
        normalized = region.strip().lower()
        return normalized in self._allowed_regions

    def filter_allowed(self, regions: Iterable[str]) -> Set[str]:
        """
        Helper that returns the subset of ``regions`` that are allowed.
        """
        return {r for r in regions if self.is_allowed(r)}