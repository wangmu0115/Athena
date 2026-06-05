"""Optional value utilities.

This module provides small helpers for working with values that may be `None`.
"""

from collections.abc import Callable


def optional_map[T, TResult](value: T | None, mapper: Callable[[T], TResult]) -> TResult | None:
    """对非 `None` 值执行映射，否则返回 `None`

    本函数仅在 `value` 不是 `None` 时调用 `mapper`，适合用于简单的 `None` 安全转换。
    """
    if value is None:
        return None
    return mapper(value)


def optional_map_or[T, TResult](
    value: T | None,
    mapper: Callable[[T], TResult],
    *,
    default: TResult,
) -> TResult:
    """对非 `None` 值执行映射，否则返回默认值

    本函数仅在 `value` 不是 `None` 时调用 `mapper`，如果 `value` 是 `None`，则直接返回 `default`。
    """
    if value is None:
        return default
    return mapper(value)


def optional_map_or_else[T, TResult](
    value: T | None,
    mapper: Callable[[T], TResult],
    *,
    default_factory: Callable[[], TResult],
) -> TResult:
    """对非 `None` 值执行映射，否则调用默认值工厂

    本函数类似于 `optional_map_or`，但会在 `value` 是 `None` 时才调用 `default_factory`，从而延迟计算回退结果。
    """
    if value is None:
        return default_factory()
    return mapper(value)


def optional_or[T](value: T | None, *, default: T) -> T:
    """返回非 `None` 值，否则返回默认值

    本函数会将 `0`、`False`、空 `str`、空 `list` 以及其他 falsy 值视为有效值，它只把 `None` 视为缺失值。
    """
    if value is None:
        return default
    return value


def optional_or_else[T](value: T | None, *, default_factory: Callable[[], T]) -> T:
    """返回非 `None` 值，否则调用默认值工厂

    本函数类似于 `optional_or`，但会在 `value` 是 `None` 时才调用 `default_factory`，从而延迟计算回退值。
    """
    if value is None:
        return default_factory()
    return value


def safe_getattr[TResult](
    value: object | None,
    attr: str,
    *,
    default: TResult | None = None,
) -> TResult | None:
    """从非 `None` 对象中获取属性，否则返回默认值

    本函数是 `getattr` 的 `None` 安全封装。如果 `value` 是 `None`，则直接返回 `default`，不会调用 `getattr`。
    """
    if value is None:
        return default
    return getattr(value, attr, default)
