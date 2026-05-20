import yaml
import logging
from pathlib import Path
from typing import Any, Dict, List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DEFAULT_IMAGE = "nginx:latest"
DEFAULT_RESOURCES = {
    "limits": {"cpu": "500m", "memory": "256Mi"},
    "requests": {"cpu": "250m", "memory": "128Mi"},
}
DEFAULT_ENV = {"name": "ENV", "value": "production"}

def load_yaml(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}

def dump_yaml(data: Dict[str, Any], path: Path) -> None:
    with path.open("w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, sort_keys=False)

def ensure_container_defaults(container: Dict[str, Any]) -> None:
    if "image" not in container:
        container["image"] = DEFAULT_IMAGE

    resources = container.setdefault("resources", {})
    limits = resources.setdefault("limits", {})
    requests = resources.setdefault("requests", {})
    for key in ("cpu", "memory"):
        limits.setdefault(key, DEFAULT_RESOURCES["limits"][key])
        requests.setdefault(key, DEFAULT_RESOURCES["requests"][key])

    env_list: List[Dict[str, str]] = container.setdefault("env", [])
    if not any(env.get("name") == DEFAULT_ENV["name"] for env in env_list):
        env_list.append(DEFAULT_ENV)

def apply_fixes(manifest: Dict[str, Any]) -> None:
    try:
        containers = manifest["spec"]["template"]["spec"]["containers"]
    except (KeyError, TypeError):
        logger.warning("Not a pod template; nothing to fix.")
        return

    if not isinstance(containers, list):
        return

    for container in containers:
        if isinstance(container, dict):
            ensure_container_defaults(container)

def main(argv: List[str]) -> None:
    if len(argv) != 2:
        print("Usage: python config_fixer.py <path-to-manifest.yaml>")
        sys.exit(1)

    path = Path(argv[1])
    if not path.is_file():
        print(f"Error: {path} does not exist or is not a file.")
        sys.exit(1)

    manifest = load_yaml(path)
    apply_fixes(manifest)
    dump_yaml(manifest, path)
    logger.info(f"Fixed configuration written to {path}")

if __name__ == "__main__":
    import sys
    main(sys.argv)