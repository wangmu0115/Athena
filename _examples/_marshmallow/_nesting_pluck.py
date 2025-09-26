from __future__ import annotations  # Enable newer type annotation syntax

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from marshmallow import Schema, fields


@dataclass
class User:
    name: str
    email: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    friends: list[User] = field(default_factory=list)
    employer: Optional[User] = None


class UserSchema(Schema):
    name = fields.String(required=True)
    email = fields.Email()
    created_at = fields.DateTime(format="%Y-%m-%d %H:%M:%S")
    friends = fields.Pluck(lambda: UserSchema, "name", many=True)
    employer = fields.Nested(lambda: UserSchema(exclude=("employer",)))
