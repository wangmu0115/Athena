from datetime import date, datetime
from zoneinfo import ZoneInfo

from athena_kit.core.temporal.codec import format_date, parse_date


def test_parse_date_iso_string():
    assert parse_date("2026-05-19") == date(2026, 5, 19)


def test_parse_date_custom_string():
    assert parse_date("20260519") == date(2026, 5, 19)


def test_parse_date_from_aware_datetime_with_timezone_conversion():
    value = datetime(2026, 5, 19, 0, 30, tzinfo=ZoneInfo("Asia/Tokyo"))

    result = parse_date(value, timezone="Asia/Shanghai")

    assert result == date(2026, 5, 18)


def test_parse_date_from_timestamp_ms():
    result = parse_date(1779165000000, timezone="Asia/Shanghai", timestamp_unit="ms")

    assert result == date(2026, 5, 19)


def test_format_date_default_formatted():
    assert format_date(date(2026, 5, 19)) == "2026-05-19"


def test_format_date_as_datetime_start_boundary():
    result = format_date(
        date(2026, 5, 19),
        timezone="Asia/Shanghai",
        output_format="datetime",
        boundary_policy="start",
    )

    assert result == datetime(2026, 5, 19, 0, 0, 0, tzinfo=ZoneInfo("Asia/Shanghai"))


def test_format_date_as_timestamp_ms():
    result = format_date(
        date(2026, 5, 19),
        timezone="Asia/Shanghai",
        output_format="timestamp_ms",
        boundary_policy="start",
    )

    assert result == 1779120000000
