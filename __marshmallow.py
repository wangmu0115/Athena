from dataclasses import dataclass, field
from datetime import datetime
from pprint import pprint

from marshmallow import Schema, fields, post_load


@dataclass
class User:
    name: str
    email: str
    is_student: bool = True
    created_at: datetime = field(default_factory=datetime.now)


class UserSchema(Schema):
    name = fields.Str()
    email = fields.Str()
    is_student = fields.Bool()
    created_at = fields.DateTime()

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)


if __name__ == "__main__":
    user = User(name="Monty", email="monty@gmail.com")
    schema = UserSchema()
    pprint(schema.dump(user))
    pprint(schema.dumps(user))
    only_schema = UserSchema(only=("name", "email"))
    pprint(only_schema.dump(user))
    pprint(only_schema.dumps(user))
    exclude_schema = UserSchema(exclude=("name",), only=("name", "email"))
    pprint(exclude_schema.dump(user))
    pprint(exclude_schema.dumps(user))

    user2 = {"created_at": "2025-09-25T14:21:24.020799", "email": "monty@gmail.com", "is_student": True, "name": "Monty"}
    print(schema.load(user2))
    print(type(user2))
    print(type(schema.load(user2)))

    user1 = User(name="Mick", email="mick@stones.com")
    user2 = User(name="Keith", email="keith@stones.com")
    users = [user1, user2]
    schema = UserSchema(many=True)
    result = schema.dump(users)  # OR UserSchema().dump(users, many=True)
    pprint(result)
