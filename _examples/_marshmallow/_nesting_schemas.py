from __future__ import annotations  # Enable newer type annotation syntax

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from marshmallow import Schema, fields


@dataclass
class User:
    name: str
    email: str
    created_at: datetime = field(default_factory=datetime.now)
    friends: list[User] = field(default_factory=list)
    employer: Optional[User] = None


@dataclass
class Blog:
    title: str
    author: User


class UserSchema(Schema):
    name = fields.String()
    email = fields.Email()
    created_at = fields.DateTime(format="%Y-%m-%d %H:%M:%S")
    friends = fields.Pluck("UserSchema", "name", many=True)


class BlogSchema(Schema):
    title = fields.String()
    author = fields.Nested(UserSchema)


class BlogSchema2(Schema):
    title = fields.String()
    author = fields.Nested(UserSchema(only=("name", "email")))


class SiteSchema(Schema):
    blog = fields.Nested(BlogSchema2)
