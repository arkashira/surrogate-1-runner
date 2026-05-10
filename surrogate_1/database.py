"""
SQLAlchemy session factory.

The default is a file‑based SQLite database so that tests can persist
between requests.  The URL can be overridden with the `DATABASE_URL`
environment variable.
"""

from __future__ import annotations

import os
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# Default to a file‑based SQLite DB in the current working directory.
DEFAULT_DB = Path.cwd() / "surrogate.db"
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DEFAULT_DB}")

engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionFactory = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
db_session = scoped_session(SessionFactory)