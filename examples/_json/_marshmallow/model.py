from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class User:
    name: str
    email: str
    is_vip: bool = False
    created_at: datetime = field(default_factory=datetime.now)
