"""Pytest configuration and shared fixtures. Uses a temporary DB so the real DB is never touched."""
import sys
from pathlib import Path

import pytest

# Ensure project root is on the path so we can import config, db, user_profile.
_root = Path(__file__).resolve().parent.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))


@pytest.fixture
def db_path(tmp_path):
    """Point the app at a temporary DB, run the schema, and yield the path. No real DB is used."""
    import config
    import db

    config.DB_PATH = tmp_path / "test.db"
    db.ensure_db()
    yield config.DB_PATH
