from datetime import date, datetime
from zoneinfo import ZoneInfo

import pytest

from athena_core.temporal.codec import DateTimeCodecOptions, format_datetime, parse_datetime


def test_parse_datetime_string_without_timezone_assumes_target_timezone():
    dt = parse_datetime("2026-05-19 12:30:00", timezone="Asia/Shanghai")
    assert dt == datetime(2026, 5, 19, 12, 30, tzinfo=ZoneInfo("Asia/Shanghai"))


def test_parse_datetime_string_ignores_naive_datetime_policy_raise():
    dt = parse_datetime(
        "2026-05-19 12:30:00",
        timezone="Asia/Shanghai",
        naive_datetime_policy="raise",
    )

    assert dt.tzinfo == ZoneInfo("Asia/Shanghai")


def test_parse_native_naive_datetime_raise():
    with pytest.raises(ValueError, match="Naive datetime"):
        parse_datetime(
            datetime(2026, 5, 19, 12, 30),
            timezone="Asia/Shanghai",
            naive_datetime_policy="raise",
        )


def test_parse_native_naive_datetime_assume_timezone():
    dt = parse_datetime(
        datetime(2026, 5, 19, 12, 30),
        timezone="Asia/Shanghai",
        naive_datetime_policy="assume_timezone",
    )

    assert dt == datetime(2026, 5, 19, 12, 30, tzinfo=ZoneInfo("Asia/Shanghai"))


def test_parse_aware_datetime_converts_timezone():
    source = datetime(2026, 5, 19, 13, 30, tzinfo=ZoneInfo("Asia/Tokyo"))

    dt = parse_datetime(source, timezone="Asia/Shanghai")

    assert dt == datetime(2026, 5, 19, 12, 30, tzinfo=ZoneInfo("Asia/Shanghai"))


def test_parse_timestamp_ms():
    dt = parse_datetime(1779165000000, timezone="Asia/Shanghai", timestamp_unit="ms")

    assert dt == datetime(2026, 5, 19, 12, 30, tzinfo=ZoneInfo("Asia/Shanghai"))


def test_parse_timestamp_s():
    dt = parse_datetime(1779165000, timezone="Asia/Shanghai", timestamp_unit="s")

    assert dt == datetime(2026, 5, 19, 12, 30, tzinfo=ZoneInfo("Asia/Shanghai"))


def test_parse_date_uses_start_boundary_by_default():
    dt = parse_datetime(date(2026, 5, 19), timezone="Asia/Shanghai")

    assert dt == datetime(2026, 5, 19, 0, 0, 0, tzinfo=ZoneInfo("Asia/Shanghai"))


def test_parse_date_uses_noon_boundary():
    dt = parse_datetime(
        date(2026, 5, 19),
        timezone="Asia/Shanghai",
        boundary_policy="noon",
    )

    assert dt == datetime(2026, 5, 19, 12, 0, 0, tzinfo=ZoneInfo("Asia/Shanghai"))


def test_format_datetime_default_options_should_work():
    value = datetime(2026, 5, 19, 12, 30, tzinfo=ZoneInfo("Asia/Shanghai"))

    result = format_datetime(
        value,
        timezone="Asia/Shanghai",
        options=DateTimeCodecOptions(output_format="formatted"),
    )

    assert result == "2026-05-19 12:30:00"


def test_format_datetime_iso():
    value = datetime(2026, 5, 19, 12, 30, tzinfo=ZoneInfo("Asia/Shanghai"))

    result = format_datetime(value, timezone="Asia/Shanghai", output_format="iso")

    assert result == "2026-05-19T12:30:00+08:00"


def test_format_datetime_timestamp_ms():
    value = datetime(2026, 5, 19, 12, 30, tzinfo=ZoneInfo("Asia/Shanghai"))

    result = format_datetime(value, timezone="Asia/Shanghai", output_format="timestamp_ms")

    assert result == 1779165000000
