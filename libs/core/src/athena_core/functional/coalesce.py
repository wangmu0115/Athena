"""Coalescing utilities.

This module provides small helpers for selecting fallback values.
These helpers are useful when a value can come from multiple sources,
such as runtime arguments, config objects, environment variables, or defaults.
"""

from typing import overload


@overload
def first_not_none[T](*values: T | None) -> T | None: ...


@overload
def first_not_none[T](*values: T | None, default: T) -> T: ...


def first_not_none[T](*values: T | None, default: T | None = None) -> T | None:
    """Return the first non-None value.

    This is similar to SQL ``COALESCE``: values are checked from left to right,
    and the first value that is not ``None`` is returned.
    """
    for value in values:
        if value is not None:
            return value
    return default
