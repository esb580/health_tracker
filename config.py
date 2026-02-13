"""Project paths and app metadata."""
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
DB_PATH = PROJECT_ROOT / "health_tracker.db"
SCHEMA_PATH = PROJECT_ROOT / "docs" / "db_schema.sql"

APP_NAME = "Health Tracker"
APP_VERSION = "1.0.0"
