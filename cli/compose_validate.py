#!/usr/bin/env python3
"""
surrogate-1 compose-validate

Validates docker-compose health checks before committing.
Usage: surrogate-1 compose-validate [-f FILE] [--quiet]
"""

import argparse
import subprocess
import sys
import time
from pathlib import Path
from typing import Optional, List, Dict, Any

DEFAULT_COMPOSE_FILE = "docker-compose.yml"
HEALTH_TIMEOUT_SECONDS = 45
HEALTH_POLL_INTERVAL_SECONDS = 2


def run_command(
    cmd: List[str], capture_output: bool = True, timeout: Optional[float] = None
) -> subprocess.CompletedProcess:
    """Run a shell command and return the completed process."""
    try:
        result = subprocess.run(
            cmd,
            capture_output=capture_output,
            text=True,
            timeout=timeout,
        )
        return result
    except subprocess.TimeoutExpired as e:
        return subprocess.CompletedProcess(cmd, -1, stdout="", stderr=str(e))
    except FileNotFoundError:
        return subprocess.CompletedProcess(cmd, 127, stdout="", stderr="Command not found")


def parse_compose_file(compose_path: Path) -> Optional[Dict[str, Any]]:
    """Parse docker-compose.yml file."""
    result = run_command(["docker-compose", "-f", str(compose_path), "config"])
    if result.returncode != 0:
        print(f"Error parsing compose file: {result.stderr}", file=sys.stderr)
        return None
    return result.stdout


def start_compose(compose_path: Path) -> bool:
    """Start the compose stack in detached mode."""
    result = run_command(
        ["docker-compose", "-f", str(compose_path), "up", "-d"],
        timeout=60,
    )
    if result.returncode != 0:
        print(f"Failed to start compose stack: {result.stderr}", file=sys.stderr)
        return False
    return True


def stop_compose(compose_path: Path) -> bool:
    """Stop the compose stack."""
    result = run_command(
        ["docker-compose", "-f", str(compose_path), "down", "-v"],
        timeout=60,
    )
    return result.returncode == 0


def get_container_ids(compose_path: Path) -> List[str]:
    """Get list of container IDs from compose stack."""
    result = run_command(
        ["docker-compose", "-f", str(compose_path), "ps", "--format", "json"],
        timeout=30,
    )
    if result.returncode != 0:
        return []
    try:
        import json
        containers = json.loads(result.stdout)
        return [c.get("ID", "") for c in containers if c.get("ID")]
    except json.JSONDecodeError:
        return []


def check_container_health(container_id: str, timeout: int) -> bool:
    """Check if a container is healthy within timeout seconds."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        result = run_command(["docker", "inspect", container_id], timeout=5)
        if result.returncode == 0:
            try:
                import json
                container_info = json.loads(result.stdout)
                if container_info:
                    status = container_info[0].get("State", {})
                    health = status.get("Health", {})
                    if health.get("Status") == "healthy":
                        return True
            except json.JSONDecodeError:
                pass
        time.sleep(1)
    return False


def validate_health_checks(
    compose_path: Path, quiet: bool = False
) -> bool:
    """Validate all containers reach healthy state."""
    container_ids = get_container_ids(compose_path)
    if not container_ids:
        if not quiet:
            print("No containers found in compose stack", file=sys.stderr)
        return False

    healthy_count = 0
    unhealthy_containers: List[str] = []

    for container_id in container_ids:
        if not check_container_health(container_id, HEALTH_TIMEOUT_SECONDS):
            unhealthy_containers.append(container_id)
        else:
            healthy_count += 1

        if not quiet:
            status = "✓" if healthy_count > 0 else "✗"
            print(f"  {status} {container_id[:12]}")

    if unhealthy_containers:
        if not quiet:
            print(f"\n{len(unhealthy_containers)} container(s) failed health check:", file=sys.stderr)
            for cid in unhealthy_containers:
                print(f"  - {cid}", file=sys.stderr)
        return False

    if not quiet:
        print(f"\nAll {healthy_count} container(s) healthy ✓")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="compose-validate",
        description="Validate docker-compose health checks before committing",
    )
    parser.add_argument(
        "-f",
        "--file",
        type=Path,
        default=DEFAULT_COMPOSE_FILE,
        help=f"Path to docker-compose.yml (default: {DEFAULT_COMPOSE_FILE})",
    )
    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="Suppress detailed output, return only exit code",
    )

    args = parser.parse_args()

    if not args.file.exists():
        print(f"Error: Compose file not found: {args.file}", file=sys.stderr)
        return 1

    if not args.file.is_file():
        print(f"Error: {args.file} is not a file", file=sys.stderr)
        return 1

    if not start_compose(args.file):
        return 1

    try:
        if validate_health_checks(args.file, quiet=args.quiet):
            return 0
        else:
            return 1
    finally:
        stop_compose(args.file)


if __name__ == "__main__":
    sys.exit(main())