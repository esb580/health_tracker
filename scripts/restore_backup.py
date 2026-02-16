#!/usr/bin/env python3
"""
Restore health_tracker.db from a backup file (health_tracker_backup.db).

Use this after you've copied your current database to health_tracker_backup.db,
or when you have a backup from another machine and want to use it as your
main database.

How to create a backup (before restoring or for safekeeping):
  - Copy health_tracker.db to health_tracker_backup.db in the project root.
  - Example (from project root): cp health_tracker.db health_tracker_backup.db

How to restore:
  1. Close the Health Tracker app if it is running (so the DB file is not in use).
  2. Put your backup file in the project root as health_tracker_backup.db.
  3. Run: python scripts/restore_backup.py
  4. The script will replace health_tracker.db with the backup. Your current
     health_tracker.db is renamed to health_tracker.db.bak (or .bak.1, .bak.2, …)
     so you can recover it if needed.
"""
import shutil
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
BACKUP_FILE = PROJECT_ROOT / "health_tracker_backup.db"
TARGET_FILE = PROJECT_ROOT / "health_tracker.db"


def main() -> None:
    if not BACKUP_FILE.exists():
        print(f"Backup file not found: {BACKUP_FILE}")
        print()
        print("To restore:")
        print("  1. Copy your backup into the project root and name it health_tracker_backup.db")
        print("  2. Close the Health Tracker app, then run this script again.")
        print()
        print("To create a backup of your current data:")
        print(f"  cp {TARGET_FILE.name} health_tracker_backup.db")
        return

    # If target exists, keep a backup of it before overwriting
    if TARGET_FILE.exists():
        bak = PROJECT_ROOT / "health_tracker.db.bak"
        if bak.exists():
            n = 1
            while (PROJECT_ROOT / f"health_tracker.db.bak.{n}").exists():
                n += 1
            bak = PROJECT_ROOT / f"health_tracker.db.bak.{n}"
        shutil.copy2(TARGET_FILE, bak)
        print(f"Current DB backed up to {bak.name}")

    shutil.copy2(BACKUP_FILE, TARGET_FILE)
    print(f"Restored {TARGET_FILE.name} from {BACKUP_FILE.name}")
    print()
    print("You can reopen the Health Tracker app.")


if __name__ == "__main__":
    main()
