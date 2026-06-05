from datetime import datetime


def is_aware_datetime(dt: datetime) -> bool:
    """判断 `datetime` 是否包含有效时区信息 (timezone-aware)。

    只有当 `tzinfo` 不为 `None` 且 `utcoffset()` 不为 `None` 时， 才认为该 `datetime` 是 aware datetime。
    """
    return dt.tzinfo is not None and dt.utcoffset() is not None


def is_naive_datetime(dt: datetime) -> bool:
    """判断 `datetime` 是否不包含有效时区信息 (timezone-naive)。"""
    return not is_aware_datetime(dt)
