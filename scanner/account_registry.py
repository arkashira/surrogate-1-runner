import os
from typing import List


def get_registered_accounts() -> List[str]:
    """
    Return a list of account identifiers that should be scanned.

    The identifiers are supplied via the ``AXENTX_ACCOUNTS`` environment
    variable as a comma‑separated list.  Leading/trailing whitespace is
    stripped and empty entries are ignored.

    Returns
    -------
    List[str]
        A list of account IDs.  If the env var is missing or empty an
        empty list is returned.
    """
    raw = os.getenv("AXENTX_ACCOUNTS", "")
    return [acct.strip() for acct in raw.split(",") if acct.strip()]