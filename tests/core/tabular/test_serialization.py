from datetime import date, datetime, time
from zoneinfo import ZoneInfo

from athena_kit.core.tabular import deserialize_cell_value, serialize_cell_value


def test_serialize_and_deserialize_scalar_values():
    assert serialize_cell_value(" value ") == "value"
    assert deserialize_cell_value("42", int) == 42
    assert deserialize_cell_value("是", bool) is True
    assert deserialize_cell_value("", str | None) is None


def test_serialize_and_deserialize_temporal_values():
    dt = datetime(2026, 5, 19, 8, 30, tzinfo=ZoneInfo("Asia/Shanghai"))

    assert serialize_cell_value(dt) == "2026-05-19T08:30:00+08:00"
    assert deserialize_cell_value("2026-05-19T08:30:00+08:00", datetime) == dt
    assert deserialize_cell_value("2026-05-19", date) == date(2026, 5, 19)
    assert deserialize_cell_value("08:30:00", time) == time(8, 30)


def test_serialize_and_deserialize_sequence_values():
    assert serialize_cell_value(["alpha", " beta "], list[str]) == "alpha, beta"
    assert deserialize_cell_value("alpha, beta", list[str]) == ["alpha", "beta"]
    assert serialize_cell_value([1, 2], list[int]) == "[1, 2]"
    assert deserialize_cell_value("[1, 2]", list[int]) == [1, 2]
    assert serialize_cell_value([1, "1", 2, "2"], list) == '[1, "1", 2, "2"]'
    assert deserialize_cell_value('[1, "1", 2, "2"]', list) == [1, "1", 2, "2"]


def test_serialize_string_tuple_values():
    assert serialize_cell_value(("alpha", " beta "), tuple[str, ...]) == "alpha, beta"
    assert serialize_cell_value(("alpha", " beta "), tuple[str, str]) == "alpha, beta"
    assert serialize_cell_value(("alpha", 1), tuple[str, int]) == '["alpha", 1]'
