-- SQLite schema for health_tracker
-- Run against your SQLite DB file (e.g. health_tracker.db) to create tables.

CREATE TABLE IF NOT EXISTS tbl_weight (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at  DATETIME NOT NULL DEFAULT (datetime('now')),
    weight      DECIMAL(6, 2) NOT NULL
);

-- Optional: index for querying by date
CREATE INDEX IF NOT EXISTS idx_tbl_weight_created_at ON tbl_weight (created_at);
