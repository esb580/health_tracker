-- SQLite schema for health_tracker
-- Run against your SQLite DB file (e.g. health_tracker.db) to create tables.

CREATE TABLE IF NOT EXISTS tbl_weight (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at  DATETIME NOT NULL DEFAULT (datetime('now')),
    weight      DECIMAL(6, 2) NOT NULL
);

-- Optional: index for querying by date
CREATE INDEX IF NOT EXISTS idx_tbl_weight_created_at ON tbl_weight (created_at);

-- Water consumption (ounces per entry, date/time stamped)
CREATE TABLE IF NOT EXISTS tbl_water (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at  DATETIME NOT NULL DEFAULT (datetime('now')),
    ounces      DECIMAL(6, 2) NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_tbl_water_created_at ON tbl_water (created_at);

-- Distance stepped (miles per entry, date/time stamped)
CREATE TABLE IF NOT EXISTS tbl_distance (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at  DATETIME NOT NULL DEFAULT (datetime('now')),
    miles       DECIMAL(6, 2) NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_tbl_distance_created_at ON tbl_distance (created_at);

-- User profile (single row per DB, id=1)
CREATE TABLE IF NOT EXISTS tbl_user_profile (
    id              INTEGER PRIMARY KEY,
    first_name      TEXT,
    last_name       TEXT,
    gender          TEXT,
    age             INTEGER,
    height_inches   REAL
);
