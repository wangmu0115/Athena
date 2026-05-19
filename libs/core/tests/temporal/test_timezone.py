from zoneinfo import ZoneInfo

import pytest

from athena_core.temporal.timezone import (
    coerce_timezone,
    get_timezone,
    set_default_timezone,
    timezone_context,
)


def test_coerce_timezone_from_string():
    assert coerce_timezone("Asia/Shanghai") == ZoneInfo("Asia/Shanghai")


def test_coerce_timezone_from_zoneinfo():
    tz = ZoneInfo("Asia/Tokyo")

    assert coerce_timezone(tz) is tz


def test_coerce_timezone_invalid_name():
    with pytest.raises(ValueError, match="Invalid timezone name"):
        coerce_timezone("Invalid/Timezone")


def test_timezone_context_temporarily_overrides_timezone():
    original = get_timezone()

    with timezone_context("Asia/Tokyo"):
        assert get_timezone() == ZoneInfo("Asia/Tokyo")

    assert get_timezone() == original


def test_set_default_timezone():
    original = get_timezone()

    try:
        set_default_timezone("Asia/Tokyo")
        assert get_timezone() == ZoneInfo("Asia/Tokyo")
    finally:
        set_default_timezone(original)
