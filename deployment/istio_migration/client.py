import json
import subprocess
import logging
from typing import List, Optional, Dict, Any

log = logging.getLogger(__name__)

class KubectlClient:
    """Executes kubectl commands and returns JSON output."""

    def __init__(self, kubeconfig: Optional[str] = None, context: Optional[str] = None):
        self.base = ["kubectl"]
        if kubeconfig:
            self.base += ["--kubeconfig", kubeconfig]
        if context:
            self.base += ["--context", context]

    def _run(self, args: List[str], input_data: Optional[str] = None) -> subprocess.CompletedProcess:
        cmd = self.base + args
        log.debug(f"Running: {' '.join(cmd)}")
        return subprocess.run(
            cmd,
            input=input_data,
            capture_output=True,
            text=True,
            check=True
        )

    def get(self, resource: str, name: str, namespace: str = "default") -> Optional[Dict[str, Any]]:
        try:
            out = self._run(["get", resource, name, "-n", namespace, "-o", "json"]).stdout
            return json.loads(out)
        except subprocess.CalledProcessError:
            return None

    def apply(self, manifest: str) -> Dict[str, Any]:
        out = self._run(["apply", "-f", "-"], input_data=manifest).stdout
        return json.loads(out)

    def delete(self, resource: str, name: str, namespace: str = "default") -> None:
        self._run(["delete", resource, name, "-n", namespace])