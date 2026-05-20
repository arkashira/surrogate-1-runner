import json
import uuid
from pathlib import Path
from typing import Optional, List, Dict, Any
from contextlib import contextmanager

from .config import settings

# Ensure directory exists on import
settings.policy_dir.mkdir(parents=True, exist_ok=True)

@contextmanager
def atomic_write(path: Path):
    """Write to a temp file then rename – guarantees atomicity."""
    tmp = path.with_suffix(".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        yield f
    tmp.replace(path)

def save_policy(policy: Dict[str, Any]) -> str:
    """Persist policy and return UUID filename."""
    policy_uuid = str(uuid.uuid4())
    filename = f"{policy_uuid}.json"
    path = settings.policy_dir / filename
    with atomic_write(path) as f:
        json.dump(policy, f, ensure_ascii=False, indent=2)
    return filename

def load_policy(filename: str) -> Optional[Dict[str, Any]]:
    path = settings.policy_dir / filename
    if not path.exists():
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def list_policies() -> List[Dict[str, Any]]:
    policies = []
    for path in settings.policy_dir.glob("*.json"):
        try:
            content = json.loads(path.read_text(encoding="utf-8"))
            policies.append({
                "filename": path.name,
                "uuid": path.stem,
                "content": content,
            })
        except json.JSONDecodeError:
            # Skip corrupted files – log later
            continue
    return policies

def delete_policy(filename: str) -> bool:
    path = settings.policy_dir / filename
    if not path.exists():
        return False
    path.unlink()
    return True