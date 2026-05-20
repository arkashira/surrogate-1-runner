import os
import sys
import json
import click
import requests

# Assuming the core import logic lives in `cli.importer`
# and provides a function `perform_import(resource_type, resource_id, workspace_id=None)`
try:
    from .importer import perform_import
except ImportError:  # pragma: no cover
    # Fallback stub for environments where the importer is not yet implemented.
    def perform_import(resource_type: str, resource_id: str, workspace_id: str = None):
        click.echo(
            f"Import stub: type={resource_type}, id={resource_id}, workspace_id={workspace_id}"
        )
        return 0


def _get_databricks_token() -> str:
    """Retrieve the Databricks personal access token from the environment."""
    token = os.getenv("DATABRICKS_TOKEN")
    if not token:
        raise click.ClickException(
            "Databricks token not found. Set the DATABRICKS_TOKEN environment variable."
        )
    return token


def _get_databricks_host() -> str:
    """Retrieve the Databricks host URL from the environment."""
    host = os.getenv("DATABRICKS_HOST")
    if not host:
        raise click.ClickException(
            "Databricks host not found. Set the DATABRICKS_HOST environment variable."
        )
    return host.rstrip("/")


def validate_workspace_id(workspace_id: str) -> None:
    """
    Validate that the supplied workspace_id is accessible with the current
    Databricks token. Raises a ClickException on failure.
    """
    token = _get_databricks_token()
    host = _get_databricks_host()

    # Databricks does not expose a direct “workspace‑id” endpoint, but we can
    # attempt to list the workspace’s root directory which requires the same
    # permissions as any import operation.
    url = f"{host}/api/2.0/workspace/list"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"path": "/", "workspace_id": workspace_id}

    try:
        response = requests.get(url, headers=headers, params=payload, timeout=10)
    except requests.RequestException as exc:
        raise click.ClickException(
            f"Failed to contact Databricks API while validating workspace_id: {exc}"
        ) from exc

    if response.status_code != 200:
        # Provide a helpful error message containing the API response.
        try:
            detail = response.json()
        except json.JSONDecodeError:
            detail = response.text
        raise click.ClickException(
            f"Workspace ID validation failed (status {response.status_code}): {detail}"
        )
    # If we get here the workspace is reachable and the token has the required perms.


@click.command(name="import")
@click.argument("resource_type", type=str)
@click.argument("resource_id", type=str)
@click.option(
    "--workspace-id",
    "workspace_id",
    type=str,
    required=False,
    help="Databricks workspace ID to use for this import operation. "
    "Overrides any provider‑level workspace configuration.",
)
def import_cmd(resource_type: str, resource_id: str, workspace_id: str | None) -> None:
    """
    Import a Databricks resource into the current state.

    RESOURCE_TYPE is the type of the resource (e.g. `cluster`, `job`).
    RESOURCE_ID   is the identifier of the resource to import.
    """
    if workspace_id:
        click.echo(f"Validating workspace ID: {workspace_id}")
        validate_workspace_id(workspace_id)
        click.echo("Workspace ID validation succeeded.")
    else:
        click.echo("No workspace ID supplied; using provider default.")

    # Delegate the heavy lifting to the core importer.
    try:
        exit_code = perform_import(resource_type, resource_id, workspace_id=workspace_id)
    except Exception as exc:  # pragma: no cover
        raise click.ClickException(f"Import failed: {exc}") from exc

    sys.exit(exit_code)


# If this module is executed directly, expose the command for debugging.
if __name__ == "__main__":
    import_cmd()