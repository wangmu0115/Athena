import json
import types
from datetime import date, datetime, time
from typing import Any, Union, get_args, get_origin

from athena_kit.core.temporal.codec import TemporalCodec


def serialize_cell_value(value: object, value_type: Any | None = None) -> Any:
    """将 Python 字段值序列化为适合写入表格单元格的值。

    该函数用于把模型字段值转换成表格后端容易保存和展示的单元格值：基础标量会原样保留，字符串会去除首尾空白，
    日期时间会格式化为稳定字符串，序列和字典会转换为逗号分隔字符串或 JSON 字符串。

    Args:
        value: 要写入表格单元格的 Python 字段值。
        value_type: 字段的类型注解。传入序列类型时，会用于决定使用逗号分隔还是 JSON 序列化。

    Returns:
        可写入表格单元格的值。
    """
    if value is None:
        return None

    value_type = _unwrap_optional(value_type) if value_type is not None else None
    temporal_codec = TemporalCodec()

    match value:
        case bool() | int() | float():
            return value
        case str():
            return value.strip()
        case datetime():
            return temporal_codec.format_datetime(value, output_format="iso")
        case date():
            return temporal_codec.format_date(value, output_format="iso")
        case time():
            return temporal_codec.format_time(value, output_format="formatted", format_pattern="%H:%M:%S")
        case list() | tuple() | set():
            return _serialize_sequence(value, value_type)
        case dict():
            return json.dumps(value, ensure_ascii=False)
        case _:
            return str(value)


def deserialize_cell_value(value: object, value_type: Any) -> Any:
    """将表格单元格值反序列化为指定类型的 Python 字段值。

    该函数用于把从表格后端读取到的单元格值还原为模型字段所需的 Python 类型。
    空单元格和空白字符串会被视为 `None`，日期时间、布尔值、序列和字典会按 `value_type` 指定的类型进行解析。

    Args:
        value: 从表格单元格读取到的原始值。
        value_type: 目标 Python 类型，通常来自模型字段的类型注解。

    Returns:
        反序列化后的 Python 字段值。
    """
    if value is None:
        return None
    if isinstance(value, str) and not value.strip():
        return None

    value_type = _unwrap_optional(value_type)
    value_type_origin = get_origin(value_type)
    temporal_codec = TemporalCodec()

    if value_type is Any:
        return value
    if value_type is str:
        return str(value).strip()
    if value_type is int:
        return _deserialize_int(value)
    if value_type is float:
        return _deserialize_float(value)
    if value_type is bool:
        return _deserialize_bool(value)
    if value_type is datetime:
        return temporal_codec.parse_datetime(str(value).strip())
    if value_type is date:
        return temporal_codec.parse_date(str(value).strip())
    if value_type is time:
        return temporal_codec.parse_time(str(value).strip())

    if value_type is list or value_type_origin is list:
        return _deserialize_sequence(value, value_type, list)
    if value_type is tuple or value_type_origin is tuple:
        return _deserialize_sequence(value, value_type, tuple)
    if value_type is set or value_type_origin is set:
        return _deserialize_sequence(value, value_type, set)

    if value_type is dict or value_type_origin is dict:
        return json.loads(str(value))

    return value


def _serialize_sequence(value: list[Any] | tuple[Any, ...] | set[Any], value_type: Any | None) -> str:
    if value_type is not None:
        if _is_str_sequence(value_type):
            return ", ".join(str(item).strip() for item in value)
        return json.dumps(list(value), ensure_ascii=False)

    return json.dumps(list(value), ensure_ascii=False)


def _deserialize_sequence(
    value: object,
    value_type: Any,
    container_cls: type,
) -> list[Any] | tuple[Any, ...] | set[Any]:
    if _is_str_sequence(value_type):  # noqa: SIM108
        items = [item.strip() for item in str(value).split(",") if item.strip()]
    else:
        items = json.loads(str(value))

    if container_cls is list:
        return list(items)
    if container_cls is tuple:
        return tuple(items)
    if container_cls is set:
        return set(items)
    raise TypeError(f"Unsupported container type: {container_cls!r}")


def _deserialize_int(value: Any) -> int:
    return int(value)


def _deserialize_float(value: Any) -> float:
    return float(value)


def _deserialize_bool(value: Any) -> bool:
    """将常见的布尔单元格值解析为 `bool`。

    - `bool` 值会原样返回
    - 数字会按 Python 真值规则转换
    - 字符串会忽略大小写和首尾空白
        - `"true"`、`"1"`、`"yes"`、`"y"`、`"是"` 会解析为 `True`
        - `"false"`、`"0"`、`"no"`、`"n"`、`"否"`、`"不是"`、`""` 会解析为 `False`
    - 无法识别的值会抛出 `ValueError`
    """
    if isinstance(value, bool):
        return value
    if isinstance(value, int | float):
        return bool(value)
    normalized = str(value).lower().strip()
    if normalized in {"true", "1", "yes", "y", "是"}:
        return True
    if normalized in {"false", "0", "no", "n", "否", "不是", ""}:
        return False
    raise ValueError(f"Cannot deserialize bool from {value!r}.")


def _unwrap_optional(tp: Any) -> Any:
    """拆开只包含一个实际类型的 Optional/Union 类型。

    示例：
        - `Optional[int]` → `int`
        - `int | None` → `int`
        - `Union[int, None]` → `int`
        - `int | str | None` → 包含多个实际类型，会保持原样
    """
    origin = get_origin(tp)
    # Optional[int], Union[int, None] → origin: typing.Union
    # int | None → origin: types.UnionType
    if origin not in {Union, types.UnionType}:
        return tp

    args = get_args(tp)
    non_none_args = [arg for arg in args if arg is not type(None)]
    if len(non_none_args) == 1:
        return non_none_args[0]

    return tp


def _is_str_sequence(tp: Any) -> bool:
    """判断类型注解是否表示字符串序列。

    会被认为是字符串序列的示例：
        - `list[str]`
        - `set[str]`
        - `tuple[str, ...]`
        - `tuple[str, str]`
        - `tuple[str, str, str]`

    不会被认为是字符串序列的示例：
        - `list`
        - `list[int]`
        - `set`
        - `set[int]`
        - `tuple`
        - `tuple[int, ...]`
        - `tuple[str, int]`
    """
    tp = _unwrap_optional(tp)
    origin = get_origin(tp)
    args = get_args(tp)
    if origin in {list, set}:
        if not args:
            return False
        return args[0] is str
    if origin is tuple:
        if not args:
            return False
        if len(args) == 2 and args[0] is str and args[1] is Ellipsis:
            return True
        return all(arg is str for arg in args)
    return False
