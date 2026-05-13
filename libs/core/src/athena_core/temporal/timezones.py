"""Timezone configuration helpers for Athena.

The module exposes a small runtime configuration API instead of a hard-coded
``DEFAULT_ZONE`` constant.  Package code should call ``get_default_timezone_name``
when constructing defaults, so applications can configure the timezone early in
startup.
"""

from __future__ import annotations

from contextlib import contextmanager
from contextvars import ContextVar, Token
from datetime import datetime
import os
from zoneinfo import ZoneInfo

DEFAULT_TIMEZONE_ENV = "ATHENA_DEFAULT_TIMEZONE"
_FALLBACK_TIMEZONE = "Asia/Shanghai"
_DEFAULT_TIMEZONE: ContextVar[str] = ContextVar(
    "ATHENA_DEFAULT_TIMEZONE",
    default=os.getenv(DEFAULT_TIMEZONE_ENV, _FALLBACK_TIMEZONE),
)


def _validate_timezone_name(timezone: str) -> str:
    """Validate an IANA timezone name and return it unchanged."""
    ZoneInfo(timezone)
    return timezone


def get_default_timezone_name() -> str:
    """Return the current Athena default timezone name."""
    return _DEFAULT_TIMEZONE.get()


def get_default_zoneinfo() -> ZoneInfo:
    """Return the current Athena default timezone as ``ZoneInfo``."""
    return ZoneInfo(get_default_timezone_name())


def set_default_timezone(timezone: str) -> Token[str]:
    """Set the default timezone for the current context.

    Args:
        timezone: IANA timezone name, for example ``"Asia/Shanghai"`` or
            ``"Europe/London"``.

    Returns:
        A ``ContextVar`` token. Pass it to ``_DEFAULT_TIMEZONE.reset(token)`` if
        you need low-level manual reset. In normal code prefer
        ``default_timezone_context``.
    """
    return _DEFAULT_TIMEZONE.set(_validate_timezone_name(timezone))


@contextmanager
def default_timezone_context(timezone: str):
    """Temporarily override Athena's default timezone in the current context."""
    token = set_default_timezone(timezone)
    try:
        yield
    finally:
        _DEFAULT_TIMEZONE.reset(token)


def normalize_datetime_timezone(value: datetime, timezone: str | ZoneInfo | None = None) -> datetime:
    """Normalize a datetime to the target timezone.

    Naive datetimes are interpreted as already being in the target timezone.
    Aware datetimes are converted with ``astimezone``.
    """
    tz = ZoneInfo(timezone) if isinstance(timezone, str) else timezone or get_default_zoneinfo()
    if value.tzinfo is None:
        return value.replace(tzinfo=tz)
    return value.astimezone(tz)
