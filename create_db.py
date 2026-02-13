#!/usr/bin/env python3
"""
Create the SQLite database and apply the schema from docs/db_schema.sql.
Run from the project root: python create_db.py
"""
import sqlite3

from config import DB_PATH, SCHEMA_PATH


def main() -> None:
    schema_sql = SCHEMA_PATH.read_text()
    conn = sqlite3.connect(DB_PATH)
    conn.executescript(schema_sql)
    conn.commit()
    conn.close()
    print(f"Database created at {DB_PATH}")


if __name__ == "__main__":
    main()
