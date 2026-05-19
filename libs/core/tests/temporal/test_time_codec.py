from datetime import datetime, time
from zoneinfo import ZoneInfo

from athena_core.temporal.codec import format_time, parse_time


def test_parse_time_iso():
    assert parse_time("12:30:15") == time(12, 30, 15)


def test_parse_time_hour_minute():
    assert parse_time("12:30") == time(12, 30)


def test_parse_time_compact():
    assert parse_time("123015") == time(12, 30, 15)


def test_parse_time_from_datetime_converts_timezone_then_extracts_time():
    value = datetime(2026, 5, 19, 13, 30, tzinfo=ZoneInfo("Asia/Tokyo"))

    result = parse_time(value, timezone="Asia/Shanghai")

    assert result == time(12, 30)


def test_format_time_default():
    assert format_time(time(12, 30, 15)) == "12:30:15"


def test_format_time_iso():
    assert format_time(time(12, 30, 15), output_format="iso") == "12:30:15"


def test_format_time_custom_pattern():
    assert format_time(time(12, 30, 15), format_pattern="%H:%M") == "12:30"
