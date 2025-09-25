from dataclasses import dataclass, field
from datetime import datetime
from pprint import pprint

from marshmallow import Schema, ValidationError, fields, post_load


@dataclass
class User:
    name: str
    email: str
    is_student: bool = True
    created_at: datetime = field(default_factory=datetime.now)


class UserSchema(Schema):
    name = fields.Str(required=True)
    email = fields.Email()
    is_student = fields.Bool()
    created_at = fields.DateTime()

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)


if __name__ == "__main__":
    user_data = [
        {"email": "mick@stones.com", "name": "Mick"},
        {"email": "invalid", "name": "Invalid"},  # invalid email
        {"email": "keith@stones.com", "name": "Keith"},
        {"email": "charlie@stones.com"},  # missing "name"
    ]
    try:
        result = UserSchema(many=True).load(user_data)
        print(result)
    except ValidationError as err:
        print("-----ValidationError-----")
        print(err.messages)  # => {"email": ['"foo" is not a valid email address.']}
        print(err.valid_data)  # => {"name": "John"}
