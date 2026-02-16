# Applying schema updates safely

The schema in `db_schema.sql` uses **only** `CREATE TABLE IF NOT EXISTS` and `CREATE INDEX IF NOT EXISTS`. That means:

- **Existing tables and data are never modified or deleted** when you apply the schema.
- New tables (and indexes) are **added** only if they don’t already exist.

So you can safely apply the current schema to your existing database without losing weight, water, or distance data.

## Option 1: Let the app do it (recommended)

1. **Back up your DB** (e.g. copy `health_tracker.db` to `health_tracker copy.db`).
2. **Run the app** (`python main.py`). On startup, `ensure_db()` runs the full schema and creates any missing tables (e.g. `tbl_distance`).
3. Your existing data stays as-is; only new, empty tables are added.

## Option 2: Apply the schema manually (no GUI)

From the project root:

```bash
sqlite3 health_tracker.db < docs/db_schema.sql
```

Use this to add new tables to an existing file without starting the app. Safe for the same reason: only missing objects are created.

## Updating a backup/copy

If you keep a copy (e.g. `health_tracker copy.db`) and want it to have the same schema (and optionally the same data):

1. **Schema only** – add new tables to the copy, keep existing data:
   ```bash
   sqlite3 "health_tracker copy.db" < docs/db_schema.sql
   ```

2. **Use the copy as your main DB** – if the copy has the data you want and the main file doesn’t:
   - Replace `health_tracker.db` with the copy (e.g. rename the copy to `health_tracker.db`), or
   - Point the app at the copy by changing `DB_PATH` in `config.py`.

No migration scripts are needed for existing data when adding new tables; the schema is additive.
