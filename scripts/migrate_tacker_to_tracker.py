#!/usr/bin/env python3
"""One-off: copy data from health_tacker.db into health_tracker.db."""
import sqlite3
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SOURCE = PROJECT_ROOT / "health_tacker.db"
TARGET = PROJECT_ROOT / "health_tracker.db"


def main() -> None:
    if not SOURCE.exists():
        print(f"Source not found: {SOURCE}")
        return

    conn_src = sqlite3.connect(SOURCE)
    conn_src.row_factory = sqlite3.Row

    conn_dst = sqlite3.connect(TARGET)

    # Copy tbl_weight
    try:
        rows = conn_src.execute(
            "SELECT created_at, weight FROM tbl_weight ORDER BY created_at"
        ).fetchall()
    except sqlite3.OperationalError as e:
        print(f"Source DB has no tbl_weight (empty or different schema): {e}")
        print("Nothing to copy.")
        conn_src.close()
        conn_dst.close()
        return

    for row in rows:
        conn_dst.execute(
            "INSERT INTO tbl_weight (created_at, weight) VALUES (?, ?)",
            (row["created_at"], row["weight"]),
        )
    weight_count = len(rows)

    # Copy tbl_water if it exists in source
    water_count = 0
    try:
        rows = conn_src.execute(
            "SELECT created_at, ounces FROM tbl_water ORDER BY created_at"
        ).fetchall()
        for row in rows:
            conn_dst.execute(
                "INSERT INTO tbl_water (created_at, ounces) VALUES (?, ?)",
                (row["created_at"], row["ounces"]),
            )
        water_count = len(rows)
    except sqlite3.OperationalError:
        pass  # no tbl_water in source

    conn_dst.commit()
    conn_src.close()
    conn_dst.close()

    print(f"Done. Copied {weight_count} weight entries and {water_count} water entries")
    print(f"  from {SOURCE.name} -> {TARGET.name}")


if __name__ == "__main__":
    main()
