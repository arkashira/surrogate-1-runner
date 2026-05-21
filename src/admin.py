from typing import List, Dict, Optional

# In a real deployment this list would be populated from a secure source
# (e.g., LDAP, IAM, or a configuration file).  For the purpose of this
# feature we keep a static list.
ADMIN_USERS = {"admin@example.com", "superuser@example.com"}

from .logging import get_audit_trail


class AuthorizationError(RuntimeError):
    """Raised when a non‑admin attempts to access audit data."""
    pass


def view_audit_trail(requesting_user: str, limit: Optional[int] = None) -> List[Dict]:
    """
    Return the audit trail for administrators.

    Parameters
    ----------
    requesting_user: str
        The identifier of the user requesting the audit data.
    limit: int | None
        Optional maximum number of entries to return.

    Returns
    -------
    List[dict]
        Audit entries ordered from newest to oldest.

    Raises
    ------
    AuthorizationError
        If ``requesting_user`` is not in ``ADMIN_USERS``.
    """
    if requesting_user not in ADMIN_USERS:
        raise AuthorizationError(f"User '{requesting_user}' is not authorized to view audit trails.")
    return get_audit_trail(limit)