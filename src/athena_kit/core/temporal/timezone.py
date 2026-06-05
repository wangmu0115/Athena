"""运行时时区配置

该模块提供了轻量级的时区运行时系统，并支持三层时区选择机制：
    1. 通过 `_timezone_context` 提供的上下文局部时区覆盖。
    2. 通过 `set_default_timezone` 配置的进程级默认时区。
    3. 从 `os.environ` 加载的环境变量默认时区。

包内部代码应优先使用 `get_timezone()` 获取当前有效时区，而不是直接导入固定的时区常量。
"""

import os
from collections.abc import Generator
from contextlib import contextmanager
from contextvars import ContextVar, Token
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

DEFAULT_TIMEZONE_NAME = "Asia/Shanghai"
"""当环境变量未提供时使用的内置默认时区名称。"""

TIMEZONE_ENV_KEYS = ("ATHENA_TIMEZONE", "ATHENA_TZ", "ATHENA__TIMEZONE", "ATHENA__TZ")
"""用于配置默认时区的环境变量名称列表。"""


@contextmanager
def timezone_context(tz: str | ZoneInfo) -> Generator[ZoneInfo, None, None]:
    """在当前上下文中临时覆盖有效时区。

    该覆盖仅作用于当前上下文，包括当前 asyncio 任务或线程上下文，并会在上下文退出时自动恢复。
    """
    zone = coerce_timezone(tz)
    token: Token[ZoneInfo | None] = _timezone_context.set(zone)

    try:
        yield zone
    finally:
        _timezone_context.reset(token)


def get_timezone() -> ZoneInfo:
    """返回当前有效时区。

    通过 `timezone_context` 设置的上下文局部时区，优先级高于进程级默认时区。
    """
    tz = _timezone_context.get()
    if tz is not None:
        return tz
    return _default_timezone


def coerce_timezone(tz: str | ZoneInfo) -> ZoneInfo:
    """将时区值转换为 `ZoneInfo` 实例。"""
    if isinstance(tz, ZoneInfo):
        return tz
    try:
        return ZoneInfo(tz)
    except ZoneInfoNotFoundError as exc:
        raise ValueError(f"Invalid timezone name: {tz}.") from exc


def _resolve_default_timezone_name() -> str:
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
    return _default_timezone


def set_default_timezone(tz: str | ZoneInfo) -> ZoneInfo:
    global _default_timezone
    _default_timezone = coerce_timezone(tz)
    return _default_timezone


def reload_default_timezone() -> ZoneInfo:
    return set_default_timezone(_resolve_default_timezone_name())
