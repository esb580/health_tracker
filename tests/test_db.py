"""Tests for the database layer: schema, weight/water/distance CRUD, and user profile."""
import pytest

# Import after conftest has run so we use the patched config when fixture is active.
# Tests that use the db_path fixture get a fresh temp DB with schema applied.


def test_ensure_db_creates_tables(db_path):
    """Schema creates expected tables so we can query them."""
    import sqlite3

    conn = sqlite3.connect(db_path)
    cursor = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
    )
    tables = {row[0] for row in cursor.fetchall()}
    conn.close()
    assert "tbl_weight" in tables
    assert "tbl_water" in tables
    assert "tbl_distance" in tables
    assert "tbl_user_profile" in tables


def test_add_weight_and_get_weight_history(db_path):
    """Adding weight entries and fetching history returns correct data."""
    import db

    db.add_weight(70.5)
    db.add_weight(71.0)
    history = db.get_weight_history()
    assert len(history) == 2
    assert history[0][1] == 70.5
    assert history[1][1] == 71.0


def test_get_weight_entries_includes_id(db_path):
    """Weight entries include id for table display and delete."""
    import db

    db.add_weight(72.0)
    entries = db.get_weight_entries()
    assert len(entries) == 1
    entry_id, created_at, weight = entries[0]
    assert entry_id >= 1
    assert weight == 72.0


def test_delete_weight_removes_entry(db_path):
    """Deleting by id removes the row and leaves others."""
    import db

    db.add_weight(70.0)
    db.add_weight(71.0)
    entries = db.get_weight_entries()
    db.delete_weight(entries[0][0])
    remaining = db.get_weight_entries()
    assert len(remaining) == 1
    assert remaining[0][2] == 71.0


def test_add_water_and_get_water_history(db_path):
    """Water entries can be added and retrieved."""
    import db

    db.add_water(16.0)
    db.add_water(8.0)
    history = db.get_water_history()
    assert len(history) == 2
    assert history[0][1] == 16.0
    assert history[1][1] == 8.0


def test_add_distance_and_get_distance_entries(db_path):
    """Distance (miles) entries can be added and retrieved."""
    import db

    db.add_distance(2.5)
    db.add_distance(1.0)
    entries = db.get_distance_entries()
    assert len(entries) == 2
    assert entries[0][2] == 2.5
    assert entries[1][2] == 1.0


def test_get_user_profile_returns_none_when_empty(db_path):
    """When no profile row exists, get_user_profile returns None."""
    import db

    assert db.get_user_profile() is None


def test_save_and_get_user_profile(db_path):
    """Saving a profile and loading it round-trips data."""
    import db
    from user_profile import UserProfile

    profile = UserProfile(
        first_name="Jane",
        last_name="Doe",
        gender="Female",
        age=30,
        height_inches=65.0,
    )
    db.save_user_profile(profile)
    loaded = db.get_user_profile()
    assert loaded is not None
    assert loaded.first_name == "Jane"
    assert loaded.last_name == "Doe"
    assert loaded.gender == "Female"
    assert loaded.age == 30
    assert loaded.height_inches == 65.0


def test_save_user_profile_overwrites_existing(db_path):
    """Saving again replaces the single profile row (id=1)."""
    import db
    from user_profile import UserProfile

    db.save_user_profile(UserProfile(first_name="Old", last_name="Name"))
    db.save_user_profile(UserProfile(first_name="New", last_name="Name"))
    loaded = db.get_user_profile()
    assert loaded is not None
    assert loaded.first_name == "New"
