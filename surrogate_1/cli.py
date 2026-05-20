"""
Command line interface for surrogate-1.

Provides a `compose-validate` subcommand that starts a Docker Compose
stack in an isolated network, waits for health checks to pass, and
exits with an appropriate status code.
"""

import argparse
import subprocess
import sys
import time
import uuid
from pathlib import Path
from typing import List, Tuple


def _run(cmd: List[str], capture_output: bool = False, check: bool = False) -> subprocess.CompletedProcess:
    """Convenience wrapper around subprocess.run."""
    return subprocess.run(
        cmd,
        stdout=subprocess.PIPE if capture_output else None,
        stderr=subprocess.PIPE if capture_output else None,
        text=True,
        check=check,
    )


def _create_network(network_name: str) -> None:
    """Create a Docker network for the validation run."""
    _run(["docker", "network", "create", network_name], check=True)


def _remove_network(network_name: str) -> None:
    """Remove the Docker network."""
    _run(["docker", "network", "rm", network_name], check=False)


def _compose_up(compose_file: Path, project_name: str, quiet: bool) -> None:
    """Start the compose stack."""
    cmd = [
        "docker",
        "compose",
        "-p",
        project_name,
        "-f",
        str(compose_file),
        "up",
        "-d",
    ]
    if quiet:
        cmd.append("--quiet-pull")
    _run(cmd, check=True)


def _compose_down(project_name: str) -> None:
    """Stop and remove the compose stack."""
    _run(
        [
            "docker",
            "compose",
            "-p",
            project_name,
            "down",
            "-v",
            "--remove-orphans",
        ],
        check=False,
    )


def _get_container_ids(project_name: str) -> List[str]:
    """Return the container IDs belonging to the given project."""
    result = _run(
        [
            "docker",
            "ps",
            "-q",
            "--filter",
            f"project={project_name}",
        ],
        capture_output=True,
        check=True,
    )
    return result.stdout.strip().splitlines()


def _inspect_health(container_id: str) -> Tuple[str, str]:
    """Return (container_name, health_status)."""
    result = _run(
        ["docker", "inspect", "--format", "{{.Name}} {{.State.Health.Status}}", container_id],
        capture_output=True,
        check=True,
    )
    name, status = result.stdout.strip().split()
    return name.lstrip("/"), status


def _wait_for_health(container_ids: List[str], timeout: int) -> Tuple[bool, List[Tuple[str, str]]]:
    """Poll containers until all are healthy or timeout expires."""
    start = time.time()
    while time.time() - start < timeout:
        unhealthy = []
        for cid in container_ids:
            try:
                name, status = _inspect_health(cid)
            except subprocess.CalledProcessError:
                # If inspect fails, treat as unhealthy
                name = cid
                status = "unknown"
            if status != "healthy":
                unhealthy.append((name, status))
        if not unhealthy:
            return True, []
        time.sleep(1)
    # Final check after timeout
    unhealthy = []
    for cid in container_ids:
        try:
            name, status = _inspect_health(cid)
        except subprocess.CalledProcessError:
            name = cid
            status = "unknown"
        if status != "healthy":
            unhealthy.append((name, status))
    return False, unhealthy


def compose_validate(args: argparse.Namespace) -> None:
    """Entry point for the compose-validate subcommand."""
    compose_file = Path(args.file).resolve()
    if not compose_file.is_file():
        print(f"Error: Compose file '{compose_file}' not found.", file=sys.stderr)
        sys.exit(1)

    # Create isolated network
    network_name = f"surrogate_validate_{uuid.uuid4().hex[:8]}"
    try:
        _create_network(network_name)
    except subprocess.CalledProcessError as e:
        print(f"Error creating Docker network: {e}", file=sys.stderr)
        sys.exit(1)

    # Use a unique project name to avoid clashes
    project_name = f"surrogate_validate_{uuid.uuid4().hex[:8]}"

    try:
        _compose_up(compose_file, project_name, args.quiet)
        container_ids = _get_container_ids(project_name)
        if not container_ids:
            print("No containers started by the compose stack.", file=sys.stderr)
            sys.exit(1)

        healthy, unhealthy = _wait_for_health(container_ids, timeout=45)
        if healthy:
            if not args.quiet:
                print("All containers are healthy.")
            sys.exit(0)
        else:
            print("Health check failed for the following containers:", file=sys.stderr)
            for name, status in unhealthy:
                print(f"  - {name}: {status}", file=sys.stderr)
            sys.exit(1)
    finally:
        # Clean up
        _compose_down(project_name)
        _remove_network(network_name)


def main(argv: List[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="surrogate-1",
        description="Surrogate-1 CLI",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # compose-validate subcommand
    validate_parser = subparsers.add_parser(
        "compose-validate",
        help="Validate Docker Compose health checks before committing.",
    )
    validate_parser.add_argument(
        "-f",
        "--file",
        default="docker-compose.yml",
        help="Path to the docker-compose.yml file (default: docker-compose.yml).",
    )
    validate_parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress detailed logs, returning only the exit code.",
    )
    validate_parser.set_defaults(func=compose_validate)

    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()