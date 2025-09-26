from dataclasses import dataclass, field
from datetime import datetime

from marshmallow import Schema, fields


@dataclass
class User:
    name: str
    email: str
    is_vip: bool = False
    created_at: datetime = field(default_factory=datetime.now)


class UserSchema(Schema):
    name = fields.String()
    email = fields.Email()
    age = fields.Integer()
    is_vip = fields.Boolean(attribute="is_vip", data_key="vip")
    created_at = fields.DateTime(format="%Y%m%d %H:%M:%S")


# Create a schema by defining a class with variables mapping attribute names to Field objects.
