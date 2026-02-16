"""User profile model for this app instance."""
from dataclasses import dataclass


@dataclass
class UserProfile:
    """User attributes for this instance (one per database)."""

    first_name: str = ""
    last_name: str = ""
    gender: str = ""
    age: int | None = None
    height_inches: float | None = None
