from typing import Callable, Optional, Union

from marshmallow import INCLUDE, Schema, ValidationError, fields, post_load


class BaseSchema(Schema):
    _data_class = None  # deserialize Python object's class

    @post_load
    def make_obj(self, data, **kwargs):
        """if `_data_class` is not None, marshamallow will try to make a `_data_class` instance, otherwise
        return dict directed.
        """
        if self._data_class is None:
            return data
        else:
            return self._data_class(**data)


class PolymorphicField(fields.Field):
    """对列表或字典中的元素根据单一属性值使用不同的模式(Schema)进行序列化和反序列化。

    Attributes:
        schemas(dict[str, Union[type[Schema], Callable[[], Schema]]]):
            不能为空。键是元素属性值，值是对元素执行序列化的 Schema，当序列化元素无对应的 Schema 时，抛出 `ValidationError` 异常。
        seri_attr(str):
            用于查找序列化 Schema 的属性名称，如果为空会尝试使用待序列化 Python 对象的类型名称。
        deseri_attr(str):
            用于查找反序列化 Schema 的 JSON 文本键名称，如果为空且 `deseri_as_dict` 为真时，会反序列化为字典类型，否则抛出 `ValidationError` 异常。
        deseri_schemas(dict[str, Union[type[Schema], Callable[[], Schema]]]):
            用于反序列化的 Schema 集合，反序列化时会根据 `deseri_attr` 先在 `deseri_schemas`中查找，如果找不到会从 `schemas` 中查找，如果都查找不到会
            根据 `deseri_as_dict` 是否为真返回字典类型，否则抛出 `ValidationError` 异常。
        deseri_as_dict(bool):
            当用于反序列化的 Schema 为空时，该属性为真时，则返回字典类型，为假时，则抛出 `ValidationError` 异常。

    Raises:
        ValidationError:
            1. 当序列化的 Python 对象无对应的 Schema 时
            2. 当反序列化的 JSON 文本不包含任何键时
            3. 当反序列化的 JSON 文本无对应的 Schema 且不允许反序列化为字典类型时
    """

    def __init__(
        self,
        schemas: dict[str, Union[type[Schema], Callable[[], Schema]]],
        seri_attr: str = "",
        deseri_attr: str = "",
        deseri_schemas: Optional[dict[str, Union[type[Schema], Callable[[], Schema]]]] = None,
        deseri_as_dict: bool = True,
        **kwargs,
    ):
        super().__init__(**kwargs)
        if schemas is None or not schemas:
            raise ValueError("serialize schemas can't be empty.")
        self.schemas = {key.lower(): value if isinstance(value, Schema) else value() for key, value in schemas.items()}
        self.seri_attr = seri_attr
        self.deseri_attr = deseri_attr
        if deseri_schemas is None or not deseri_schemas:
            self.deseri_schemas = {}
        else:
            self.deseri_schemas = {key.lower(): value if isinstance(value, Schema) else value() for key, value in deseri_schemas.items()}
        self.deseri_as_dict = deseri_as_dict

    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        if self.seri_attr:  # 获取匹配 Schema 的键
            schema_key = getattr(value, self.seri_attr).lower()
        else:
            schema_key = type(value).__name__.lower()
        if schema_key not in self.schemas:
            raise ValidationError(f"unknown serializes type: {schema_key}")
        else:
            return self.schemas[schema_key].dump(value)

    def _deserialize(self, value, attr, data, **kwargs):
        if not isinstance(value, dict):  # 非字典类型，抛出异常
            raise ValidationError(f"{value} must be dict.")
        schema_key = value.get(self.deseri_attr, "").lower()
        if schema_key is not None and (schema_key in self.deseri_schemas or schema_key in self.schemas):
            schema = self.deseri_schemas.get(schema_key, self.schemas.get(schema_key))
            try:
                return schema.load(value)
            except TypeError:
                if self.deseri_as_dict:
                    return Schema.from_dict({})(unknown=INCLUDE).load(value)
                raise
        elif self.deseri_as_dict:
            return Schema.from_dict({})(unknown=INCLUDE).load(value)
        else:
            raise ValidationError(f"unknown deserializes type: {schema_key}")
