"""
Asyncpg connection‑pool wrapper.

The pool is created lazily on first use and cached for the lifetime
of the process.  The connection string is read from
`DATABASE_URL` (e.g. `postgresql://user:pass@host/dbname`).
"""

import os
from asyncpg import create_pool, Pool

_pool: Pool | None = None


async def get_pool() -> Pool:
    global _pool
    if _pool is None:
        _pool = await create_pool(os.getenv("DATABASE_URL", "postgresql://localhost"))
    return _pool