"""Timezone utilities for runtime configuration and datetime normalization.

This module provides a lightweight timezone runtime for Athena.

It supports three levels of timezone selection:
    1. Context-local timezone override via ``timezone_context``.
    2. Process-wide default timezone configured by ``set_default_timezone``.
    3. Environment-based default timezone loaded from ``os.environ``.

The module intentionally does not load ``.env`` files by itself. Applications
that use ``python-dotenv`` should call ``load_dotenv()`` before importing or
reloading this module's default timezone.

Package code should prefer ``get_timezone()`` over importing a fixed timezone
constant directly. This allows timezone behavior to be controlled by environment
variables, application startup code, or temporary context-local overrides.
"""

import os
from collections.abc import Generator
from contextlib import contextmanager
from contextvars import ContextVar, Token
from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

DEFAULT_TIMEZONE_NAME = "Asia/Shanghai"
"""Built-in fallback timezone name used when no environment override exists."""

TIMEZONE_ENV_KEYS = ("ATHENA_TIMEZONE", "ATHENA_TZ", "ATHENA__TIMEZONE", "ATHENA__TZ")
"""Environment variable names used to configure the default timezone."""


def coerce_timezone(tz: str | ZoneInfo) -> ZoneInfo:
    """Coerce a timezone value into a ``ZoneInfo`` instance."""
    if isinstance(tz, ZoneInfo):
        return tz

    try:
        return ZoneInfo(tz)
    except ZoneInfoNotFoundError as exc:
        raise ValueError(f"Invalid timezone name: {tz}.") from exc


def _resolve_default_timezone_name() -> str:
    """Resolve the process-wide default timezone name from environment variables."""
    for tz_key in TIMEZONE_ENV_KEYS:
        tz_name = os.getenv(tz_key)
        if tz_name:
            return tz_name

    return DEFAULT_TIMEZONE_NAME


_default_timezone: ZoneInfo = coerce_timezone(_resolve_default_timezone_name())

_timezone_context: ContextVar[ZoneInfo | None] = ContextVar(
    "athena_timezone",
    default=None,
)


def get_default_timezone() -> ZoneInfo:
    """Return the process-wide default timezone."""
    return _default_timezone


def set_default_timezone(timezone: str | ZoneInfo) -> ZoneInfo:
    """Set the process-wide default timezone."""
    global _default_timezone

    _default_timezone = coerce_timezone(timezone)
    return _default_timezone


def reload_default_timezone() -> ZoneInfo:
    """Reload the process-wide default timezone from environment variables."""
    return set_default_timezone(_resolve_default_timezone_name())


def get_timezone() -> ZoneInfo:
    """Return the currently effective timezone.

    The context-local timezone set by ``timezone_context`` takes precedence over
    the process-wide default timezone.
    """
    timezone = _timezone_context.get()

    if timezone is not None:
        return timezone

    return _default_timezone


def is_aware_datetime(dt: datetime) -> bool:
    """Return whether a ``datetime`` is timezone-aware.

    A ``datetime`` is considered aware only when ``tzinfo`` is not ``None`` and
    ``utcoffset()`` also returns a non-``None`` value.
    """
    return dt.tzinfo is not None and dt.utcoffset() is not None


def normalize_datetime_timezone(dt: datetime, *, tz: str | ZoneInfo | None = None) -> datetime:
    """Normalize a datetime to the target timezone.

    If ``dt`` is naive, it is interpreted as already being in the target
    timezone and the timezone is attached with ``replace(tzinfo=...)``.

    If ``dt`` is aware, it is converted to the target timezone with ``astimezone(...)``.
    """
    target_tz = coerce_timezone(tz) if tz is not None else get_timezone()
    if is_aware_datetime(dt):
        return dt.astimezone(target_tz)

    return dt.replace(tzinfo=target_tz)


@contextmanager
def timezone_context(tz: str | ZoneInfo) -> Generator[ZoneInfo, None, None]:
    """Temporarily override the effective timezone in the current context.

    The override is local to the current context, including the current asyncio
    task or thread context. It is restored automatically when the context exits.
    """
    zone = coerce_timezone(tz)
    token: Token[ZoneInfo | None] = _timezone_context.set(zone)

    try:
        yield zone
    finally:
        _timezone_context.reset(token)
