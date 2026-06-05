import pytest

from athena_kit.bosun.opentsdb.enums import Aggregator, FilterType, MultiFunction
from athena_kit.bosun.opentsdb.exceptions import OpenTSDBParseError
from athena_kit.bosun.opentsdb.models import Query
from athena_kit.bosun.opentsdb.parser import (
    parse_downsampling,
    parse_multifield,
    parse_query,
    parse_rate,
    parse_tagkv,
    parse_topk,
)


def test_parse_downsampling_normalizes_default_fill_policy():
    downsampling = parse_downsampling("1m-avg")

    assert downsampling is not None
    assert downsampling.interval == "1m"
    assert downsampling.aggregator == Aggregator.AVG
    assert downsampling.fill_policy == "none"
    assert str(downsampling) == "1m-avg-none"


def test_parse_downsampling_returns_none_for_other_components():
    assert parse_downsampling("rate{counter}") is None


def test_parse_downsampling_rejects_invalid_aggregator():
    with pytest.raises(OpenTSDBParseError, match="Illegal OpenTSDB component"):
        parse_downsampling("1m-unknown")


def test_parse_rate_variants():
    plain_rate = parse_rate("rate")
    counter_rate = parse_rate("rate{counter}")
    full_rate = parse_rate("rate{counter,,,diff,after_downsample}")

    assert plain_rate is not None
    assert plain_rate.counter is False
    assert plain_rate.delta is False
    assert counter_rate is not None
    assert counter_rate.counter is True
    assert counter_rate.delta is False
    assert full_rate is not None
    assert full_rate.counter is True
    assert full_rate.delta is True
    assert full_rate.downsample == "after_downsample"
    assert parse_rate("top-10-max") is None


def test_parse_rate_rejects_malformed_rate_prefix():
    with pytest.raises(OpenTSDBParseError, match="Illegal rate string"):
        parse_rate("rate {counter}")


def test_parse_topk_variants():
    topk = parse_topk("bottom-5-avg")

    assert topk is not None
    assert topk.top_bottom == "bottom"
    assert topk.num == 5
    assert topk.option == "avg"
    assert str(topk) == "bottom-5-avg"
    assert parse_topk("rate") is None


def test_parse_topk_rejects_invalid_num():
    with pytest.raises(OpenTSDBParseError, match="Illegal topk string"):
        parse_topk("top-many-max")


def test_parse_tagkv_defaults_to_literal_or():
    tagkv = parse_tagkv("host=a|b", group_by=True)

    assert tagkv.key == "host"
    assert tagkv.values == ["a", "b"]
    assert tagkv.filter_type == FilterType.LITERAL_OR
    assert tagkv.group_by is True
    assert str(tagkv) == "host=literal_or(a|b)"


def test_parse_tagkv_with_explicit_filter_type():
    tagkv = parse_tagkv("host=not_literal_or(a|b)")

    assert tagkv.filter_type == FilterType.NOT_LITERAL_OR
    assert tagkv.values == ["a", "b"]


def test_parse_multifield_plain_fields():
    multifield = parse_multifield("rt.pct90,count.rate")

    assert multifield.fields == ["rt.pct90", "count.rate"]
    assert multifield.field_func is None
    assert str(multifield) == "count.rate,rt.pct90"


def test_parse_multifield_function_call():
    multifield = parse_multifield("weighted_avg(value=rt.pct90,weight=count)")

    assert multifield.field_func == MultiFunction.WEIGHTED_AVG
    assert multifield.func_params == {"value": "rt.pct90", "weight": "count"}
    assert multifield.fields == ["rt.pct90", "count"]
    assert str(multifield) == "weighted_avg(value=rt.pct90,weight=count)"


def test_parse_full_query_with_optional_components():
    query = parse_query(
        "sum:1m-avg:rate{counter,,,diff,after_downsample}:top-10-max:"
        "[tenant]service.latency{host=a|b}{env=prod}[rt.pct90,count.rate]"
    )

    assert query.aggregator == Aggregator.SUM
    assert query.tenant == "tenant"
    assert query.metric == "service.latency"
    assert query.downsampling is not None
    assert query.rate is not None
    assert query.topk is not None
    assert query.groups[0].group_by is True
    assert query.filters[0].group_by is False
    assert str(query) == (
        "sum:1m-avg-none:rate{counter,,,diff,after_downsample}:top-10-max:"
        "[tenant]service.latency{host=literal_or(a|b)}{env=literal_or(prod)}[count.rate,rt.pct90]"
    )


def test_query_classmethod_delegates_to_parser():
    query = Query.parse_query("sum:service.qps")

    assert isinstance(query, Query)
    assert str(query) == "sum:[default]service.qps{}{}"


def test_parse_query_rejects_empty_string():
    with pytest.raises(OpenTSDBParseError, match="query string is empty"):
        parse_query("")
