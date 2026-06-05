import json
import types
from datetime import date, datetime, time
from typing import Any, Union, get_args, get_origin

from athena_core.temporal.timezone import get_timezone

DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S%z"
DATE_FORMAT = "%Y-%m-%d"
TIME_FORMAT = "%H:%M:%S"


def encode_field_value(field_value: Any, field_type: Any | None = None) -> Any:
    """Encode a Pydantic model field value into a table cell value."""
    if field_value is None:
        return None

    field_type = _unwrap_optional(field_type) if field_type is not None else None

    match field_value:
        case bool() | int() | float():
            return field_value
        case str():
            return field_value.strip()
        case datetime():
            value = field_value
            if value.tzinfo is None:
                value = value.replace(tzinfo=get_timezone())
            return value.strftime(DATETIME_FORMAT)
        case date():
            return field_value.strftime(DATE_FORMAT)
        case time():
            return field_value.strftime(TIME_FORMAT)
        case list() | tuple() | set():
            return _encode_sequence(field_value, field_type)
        case dict():
            return json.dumps(field_value, ensure_ascii=False)
        case _:
            return str(field_value)


def decode_cell_value(cell_value: Any, field_type: Any) -> Any:
    """Decode a table cell value into a Pydantic model field value."""
    if cell_value is None:
        return None
    if isinstance(cell_value, str) and not cell_value.strip():
        return None

    field_type = _unwrap_optional(field_type)
    field_type_origin = get_origin(field_type)

    if field_type is Any:
        return cell_value
    if field_type is str:
        return str(cell_value).strip()
    if field_type is int:
        return int(cell_value)
    if field_type is float:
        return float(cell_value)
    if field_type is bool:
        return _decode_bool(cell_value)
    if field_type is datetime:
        return datetime.strptime(str(cell_value).strip(), DATETIME_FORMAT)
    if field_type is date:
        return datetime.strptime(str(cell_value).strip(), DATE_FORMAT).date()
    if field_type is time:
        return datetime.strptime(str(cell_value).strip(), TIME_FORMAT).time()

    if field_type is list or field_type_origin is list:
        return _decode_sequence(cell_value, field_type, list)
    if field_type is tuple or field_type_origin is tuple:
        return _decode_sequence(cell_value, field_type, tuple)
    if field_type is set or field_type_origin is set:
        return _decode_sequence(cell_value, field_type, set)

    if field_type is dict or field_type_origin is dict:
        return json.loads(str(cell_value))

    return cell_value


def _encode_sequence(value: list[Any] | tuple[Any, ...] | set[Any], value_type: Any | None) -> str:
    if value_type is not None:
        if _is_str_sequence(value_type):
            return ", ".join(str(item).strip() for item in value)
        return json.dumps(list(value), ensure_ascii=False)

    if all(isinstance(item, str) for item in value):
        return ", ".join(str(item).strip() for item in value)

    return json.dumps(list(value), ensure_ascii=False)


def _decode_sequence(value: Any, value_type: Any, container_cls: type) -> list[Any] | tuple[Any, ...] | set[Any]:
    if _is_str_sequence(value_type):
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


def _decode_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, int | float):
        return bool(value)
    normalized = str(value).lower().strip()
    if normalized in {"true", "1", "yes", "y", "是"}:
        return True
    if normalized in {"false", "0", "no", "n", "否", "不是", ""}:
        return False
    raise ValueError(f"Cannot decode bool from {value!r}")


def _unwrap_optional(tp: Any) -> Any:
    origin = get_origin(tp)
    if origin not in {Union, types.UnionType}:
        return tp

    args = get_args(tp)
    non_none_args = [arg for arg in args if arg is not type(None)]
    if len(non_none_args) == 1:
        return non_none_args[0]

    return tp


def _is_str_sequence(tp: Any) -> bool:
    tp = _unwrap_optional(tp)
    origin = get_origin(tp)
    args = get_args(tp)
    if tp in {list, tuple, set}:
        return True
    if origin in {list, set}:
        return not args or args[0] is str
    if origin is tuple:
        if not args:
            return True
        return len(args) == 2 and args[0] is str and args[1] is Ellipsis
    return False
