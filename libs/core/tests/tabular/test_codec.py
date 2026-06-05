from datetime import date, datetime, time
from zoneinfo import ZoneInfo

from athena_core.tabular import decode_cell_value, encode_field_value


def test_encode_and_decode_scalar_values():
    assert encode_field_value(" value ") == "value"
    assert decode_cell_value("42", int) == 42
    assert decode_cell_value("是", bool) is True
    assert decode_cell_value("", str | None) is None


def test_encode_and_decode_temporal_values():
    dt = datetime(2026, 5, 19, 8, 30, tzinfo=ZoneInfo("Asia/Shanghai"))

    assert encode_field_value(dt) == "2026-05-19T08:30:00+0800"
    assert decode_cell_value("2026-05-19T08:30:00+0800", datetime) == dt
    assert decode_cell_value("2026-05-19", date) == date(2026, 5, 19)
    assert decode_cell_value("08:30:00", time) == time(8, 30)


def test_encode_and_decode_sequence_values():
    assert encode_field_value(["alpha", " beta "], list[str]) == "alpha, beta"
    assert decode_cell_value("alpha, beta", list[str]) == ["alpha", "beta"]
    assert encode_field_value([1, 2], list[int]) == "[1, 2]"
    assert decode_cell_value("[1, 2]", list[int]) == [1, 2]
