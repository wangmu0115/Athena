from enum import IntEnum, StrEnum
from typing import Any, ClassVar, Self


class LabelEnumMixin[ValueT: (int, str)]:
    """为枚举类增加标签和别名查询能力的 Mixin。

    该 Mixin 适合与 `IntEnum` 或 `StrEnum` 组合使用，用于让枚举成员同时具备：
        - 原始枚举值：`value`
        - 展示标签：`label`
        - 查询别名：`aliases`

    枚举成员应按如下格式声明：
    ```python
    MEMBER = value, label, alias1, alias2, ...
    ```
    """

    label: str
    aliases: tuple[str, ...]

    _label_map_cs: ClassVar[dict[str, Any]]  # case-sensitive
    _label_map_ci: ClassVar[dict[str, Any]]  # case-insensitive

    def __init_subclass__(cls, **kwargs: Any):
        super().__init_subclass__(**kwargs)

        case_sensitive_map: dict[str, Any] = {}
        case_insensitive_map: dict[str, Any] = {}

        for item in cls:
            texts = (item.label, *item.aliases)
            for text in texts:
                if text in case_sensitive_map and case_sensitive_map[text] is not item:
                    raise ValueError(f"Duplicate label or alias: {text}.")
                case_sensitive_map[text] = item

                text_ci = text.casefold()
                if text_ci in case_insensitive_map and case_insensitive_map[text_ci] is not item:
                    raise ValueError(f"Duplicate label or alias case-insensitively: {text}.")
                case_insensitive_map[text_ci] = item

        cls._label_map_cs = case_sensitive_map
        cls._label_map_ci = case_insensitive_map

    @classmethod
    def safe_from_value(cls, value: ValueT | None) -> Self | None:
        """根据原始值安全获取枚举成员。"""
        if value is None:
            return None
        return cls._value2member_map_.get(value)

    @classmethod
    def from_value(cls, value: ValueT) -> Self:
        """根据原始值获取枚举成员。

        Raises:
            ValueError: 当 `value` 不是合法枚举值时抛出。
        """
        return cls(value)

    @classmethod
    def safe_from_label(cls, label: str | None, *, case_sensitive: bool = True) -> Self | None:
        """根据标签或别名安全获取枚举成员。"""
        if label is None:
            return None

        if case_sensitive:
            return cls._label_map_cs.get(label)

        return cls._label_map_ci.get(label.casefold())

    @classmethod
    def from_label(cls, label: str, *, case_sensitive: bool = True) -> Self:
        """根据标签或别名获取枚举成员。

        Raises:
            ValueError: 当 `label` 不是合法标签或别名时抛出。
        """
        item = cls.safe_from_label(label, case_sensitive=case_sensitive)
        if item is None:
            raise ValueError(f"{label} is not a valid label/alias for {cls.__name__}.")
        return item

    def to_dict(self) -> dict[str, Any]:
        """将枚举成员转换为包含 `name`、`value`、`label` 和 `aliases` 的字典。"""
        return {
            "name": self.name,
            "value": self.value,
            "label": self.label,
            "aliases": self.aliases,
        }


class LabelIntEnum(LabelEnumMixin[int], IntEnum):
    """带标签和别名能力的整数枚举基类，枚举值类型为 `int`。"""

    def __new__(cls, value: int, label: str, *aliases: str):
        obj = int.__new__(cls, value)
        obj._value_ = value
        obj.label = label
        obj.aliases = tuple(aliases)
        return obj


class LabelStrEnum(LabelEnumMixin[str], StrEnum):
    """带标签和别名能力的字符串枚举基类，枚举值类型为 `str`。"""

    def __new__(cls, value: str, label: str, *aliases: str):
        obj = str.__new__(cls, value)
        obj._value_ = value
        obj.label = label
        obj.aliases = tuple(aliases)
        return obj
