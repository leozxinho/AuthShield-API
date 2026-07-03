from dataclasses import dataclass
from datetime import datetime


@dataclass
class User:
    id: int
    name: str
    email: str
    password_hash: str
    is_verified: bool = False
    password_changed_at: datetime | None = None
    verification_token: str | None = None
    is_active: bool = True
    created_at: datetime | None = None
    failed_login_attempts: int = 0
    locked_until: datetime | None = None
