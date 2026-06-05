"""Value coalesce utilities.

This module provides small, explicit helpers for selecting the first usable value
from a group of candidates.
"""

from collections.abc import Callable, Sized

_MISSING = object()


def first_not_none[T](*values: T | None, default: Callable[[], T] | T | object = _MISSING) -> T | None:
    """返回第一个非 `None` 值

    本函数只跳过 `None`，其他 falsy 值，例如 `0`、`False`、`""`、`[]` 和 `{}` 都会被视为有效值。
    """
    for value in values:
        if value is not None:
            return value

    if default is _MISSING:
        return None
    return _resolve_default(default)


def first_non_empty[T: Sized](*values: T | None, default: Callable[[], T] | T | object = _MISSING) -> T | None:
    """返回第一个非空的 Sized 值

    当 `len(value) > 0` 时，该值被认为是非空，主要用于容器和字符串，例如 `str`、`list`、`tuple`、`dict` 和 `set` 等。

    `None` 总是会被跳过，不应将 `int`、`bool` 等非 Sized 类型传入本函数。
    """
    for value in values:
        if value is not None and len(value) > 0:
            return value

    if default is _MISSING:
        return None
    return _resolve_default(default)


def first_truthy[T](*values: T, default: Callable[[], T] | T | object = _MISSING) -> T | None:
    """返回第一个 truthy 值

    本函数遵循 Python 的真值测试规则，`None`、`False`、`0`、`""`、`[]` 和 `{}` 等值都会被跳过。

    仅当你明确需要 Python truthiness 语义时才使用本函数，如果只是想跳过 `None`，请使用 `first_not_none`。
    """
    for value in values:
        if value:
            return value

    if default is _MISSING:
        return None
    return _resolve_default(default)


def _resolve_default[T](default: Callable[[], T] | T) -> T:

    return default() if callable(default) else default
