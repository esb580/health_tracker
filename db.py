"""Database access for weight, water, distance, and user profile."""
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any

import config
from user_profile import UserProfile


def get_connection() -> sqlite3.Connection:
    """Return a connection to the SQLite database."""
    return sqlite3.connect(config.DB_PATH)


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


def get_weight_entries() -> list[tuple[int, datetime, float]]:
    """Return all weight entries as (id, created_at, weight) ordered by date."""
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT id, created_at, weight FROM tbl_weight ORDER BY created_at"
    ).fetchall()
    conn.close()
    result: list[tuple[int, datetime, float]] = []
    for row in rows:
        ts = row["created_at"]
        if isinstance(ts, str):
            try:
                dt = datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        else:
            dt = ts
        result.append((int(row["id"]), dt, float(row["weight"])))
    return result


def delete_weight(entry_id: int) -> None:
    """Delete a weight entry by id."""
    conn = get_connection()
    conn.execute("DELETE FROM tbl_weight WHERE id = ?", (entry_id,))
    conn.commit()
    conn.close()


def add_water(ounces: float) -> None:
    """Insert a water entry (created_at defaults to now)."""
    conn = get_connection()
    conn.execute(
        "INSERT INTO tbl_water (ounces) VALUES (?)",
        (round(ounces, 2),),
    )
    conn.commit()
    conn.close()


def get_water_history() -> list[tuple[datetime, float]]:
    """Return all water entries as (created_at, ounces) ordered by date."""
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT created_at, ounces FROM tbl_water ORDER BY created_at"
    ).fetchall()
    conn.close()
    result: list[tuple[datetime, float]] = []
    for row in rows:
        ts = row["created_at"]
        if isinstance(ts, str):
            try:
                dt = datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        else:
            dt = ts
        result.append((dt, float(row["ounces"])))
    return result


def get_water_entries() -> list[tuple[int, datetime, float]]:
    """Return all water entries as (id, created_at, ounces) ordered by date."""
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT id, created_at, ounces FROM tbl_water ORDER BY created_at"
    ).fetchall()
    conn.close()
    result: list[tuple[int, datetime, float]] = []
    for row in rows:
        ts = row["created_at"]
        if isinstance(ts, str):
            try:
                dt = datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        else:
            dt = ts
        result.append((int(row["id"]), dt, float(row["ounces"])))
    return result


def delete_water(entry_id: int) -> None:
    """Delete a water entry by id."""
    conn = get_connection()
    conn.execute("DELETE FROM tbl_water WHERE id = ?", (entry_id,))
    conn.commit()
    conn.close()


def add_distance(miles: float) -> None:
    """Insert a distance (miles) entry (created_at defaults to now)."""
    conn = get_connection()
    conn.execute(
        "INSERT INTO tbl_distance (miles) VALUES (?)",
        (round(miles, 2),),
    )
    conn.commit()
    conn.close()


def get_distance_history() -> list[tuple[datetime, float]]:
    """Return all distance entries as (created_at, miles) ordered by date."""
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT created_at, miles FROM tbl_distance ORDER BY created_at"
    ).fetchall()
    conn.close()
    result: list[tuple[datetime, float]] = []
    for row in rows:
        ts = row["created_at"]
        if isinstance(ts, str):
            try:
                dt = datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        else:
            dt = ts
        result.append((dt, float(row["miles"])))
    return result


def get_distance_entries() -> list[tuple[int, datetime, float]]:
    """Return all distance entries as (id, created_at, miles) ordered by date."""
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT id, created_at, miles FROM tbl_distance ORDER BY created_at"
    ).fetchall()
    conn.close()
    result: list[tuple[int, datetime, float]] = []
    for row in rows:
        ts = row["created_at"]
        if isinstance(ts, str):
            try:
                dt = datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        else:
            dt = ts
        result.append((int(row["id"]), dt, float(row["miles"])))
    return result


def delete_distance(entry_id: int) -> None:
    """Delete a distance entry by id."""
    conn = get_connection()
    conn.execute("DELETE FROM tbl_distance WHERE id = ?", (entry_id,))
    conn.commit()
    conn.close()


_USER_PROFILE_ID = 1


def get_user_profile() -> UserProfile | None:
    """Return the user profile row if it exists, else None."""
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    row = conn.execute(
        "SELECT first_name, last_name, gender, age, height_inches FROM tbl_user_profile WHERE id = ?",
        (_USER_PROFILE_ID,),
    ).fetchone()
    conn.close()
    if row is None:
        return None
    return UserProfile(
        first_name=row["first_name"] or "",
        last_name=row["last_name"] or "",
        gender=row["gender"] or "",
        age=row["age"] if row["age"] is not None else None,
        height_inches=row["height_inches"] if row["height_inches"] is not None else None,
    )


def save_user_profile(profile: UserProfile) -> None:
    """Insert or replace the single user profile row (id=1)."""
    conn = get_connection()
    conn.execute(
        """INSERT OR REPLACE INTO tbl_user_profile (id, first_name, last_name, gender, age, height_inches)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (
            _USER_PROFILE_ID,
            profile.first_name or None,
            profile.last_name or None,
            profile.gender or None,
            profile.age,
            profile.height_inches,
        ),
    )
    conn.commit()
    conn.close()
