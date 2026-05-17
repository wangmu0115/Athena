"""Optional value helpers.

This module provides small utilities for working with optional values.

The main use case is applying a transformation only when the source value is
not ``None``. This is similar to ``Optional.map`` in other languages, but keeps
the API explicit and Python-friendly.
"""

from collections.abc import Callable


def map_optional[T, TResult](
    value: T | None,
    mapper: Callable[[T], TResult],
) -> TResult | None:
    """Map an optional value.

    Applies ``mapper`` only when ``value`` is not ``None``. If ``value`` is
    ``None``, the function returns ``None`` directly.

    Examples:
        >>> class User:
        ...     def __init__(self, name: str) -> None:
        ...         self.name = name
        >>> user = User("Alice")
        >>> map_optional(user, lambda x: x.name)
        'Alice'
        >>> map_optional(None, lambda x: x.name)
        None
    """
    if value is None:
        return None
    return mapper(value)


def map_optional_or[T, TResult](
    value: T | None,
    mapper: Callable[[T], TResult],
    *,
    default: TResult,
) -> TResult:
    """Map an optional value with a fallback default.

    Applies ``mapper`` only when ``value`` is not ``None``. If ``value`` is
    ``None``, returns ``default``.

    Args:
        value: Source value to transform.
        mapper: Mapping function applied to the non-None value.
        default: Fallback value returned when ``value`` is ``None``.

    Returns:
        The mapped value if ``value`` is not ``None``; otherwise ``default``.

    Examples:
        >>> class User:
        ...     def __init__(self, name: str) -> None:
        ...         self.name = name
        >>> user = User("Alice")
        >>> map_optional_or(user, lambda x: x.name, default="anonymous")
        'Alice'
        >>> map_optional_or(None, lambda x: x.name, default="anonymous")
        'anonymous'
    """
    if value is None:
        return default
    return mapper(value)


def get_optional_attr[TResult](
    value: object | None,
    attr: str,
    *,
    default: TResult | None = None,
) -> TResult | None:
    """Safely get an attribute from an optional object.

    If ``value`` is ``None``, returns ``default``. Otherwise, this function
    returns ``getattr(value, attr, default)``.

    Prefer ``map_optional(value, lambda x: x.attr)`` when you want better type
    checking and IDE support.

    Args:
        value: Object to read from.
        attr: Attribute name.
        default: Fallback value returned when ``value`` is ``None`` or the
            attribute does not exist.

    Returns:
        The attribute value if available; otherwise ``default``.

    Examples:
        >>> class User:
        ...     def __init__(self, name: str) -> None:
        ...         self.name = name
        >>> user = User("Alice")
        >>> get_optional_attr(user, "name")
        'Alice'
        >>> get_optional_attr(None, "name")
        None
        >>> get_optional_attr(user, "missing", default="unknown")
        'unknown'
    """
    if value is None:
        return default
    return getattr(value, attr, default)
