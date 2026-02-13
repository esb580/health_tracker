"""Database access for weight entries."""
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any

from config import DB_PATH


def get_connection() -> sqlite3.Connection:
    """Return a connection to the SQLite database."""
    return sqlite3.connect(DB_PATH)


def ensure_db() -> None:
    """Create DB and schema if they do not exist."""
    from config import SCHEMA_PATH
    conn = get_connection()
    conn.executescript(SCHEMA_PATH.read_text())
    conn.commit()
    conn.close()


def add_weight(weight: float) -> None:
    """Insert a weight entry (created_at defaults to now)."""
    conn = get_connection()
    conn.execute(
        "INSERT INTO tbl_weight (weight) VALUES (?)",
        (round(weight, 2),),
    )
    conn.commit()
    conn.close()


def get_weight_history() -> list[tuple[datetime, float]]:
    """Return all weight entries as (created_at, weight) ordered by date."""
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT created_at, weight FROM tbl_weight ORDER BY created_at"
    ).fetchall()
    conn.close()
    result: list[tuple[datetime, float]] = []
    for row in rows:
        ts = row["created_at"]
        if isinstance(ts, str):
            # SQLite returns datetime as "YYYY-MM-DD HH:MM:SS"
            try:
                dt = datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        else:
            dt = ts
        result.append((dt, float(row["weight"])))
    return result
