from datetime import datetime


def is_aware_datetime(dt: datetime) -> bool:
    """Return whether a `datetime` is timezone-aware."""
    return dt.tzinfo is not None and dt.utcoffset() is not None


def is_naive_datetime(dt: datetime) -> bool:
    """Return whether a `datetime` is timezone-naive."""
    return not is_aware_datetime(dt)
