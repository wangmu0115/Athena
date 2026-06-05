import pytest
from pydantic import ValidationError

from athena_kit.bosun.opentsdb.enums import Aggregator, FilterType
from athena_kit.bosun.opentsdb.intervals import calc_interval_seconds
from athena_kit.bosun.opentsdb.models import Downsampling, MultiField, Query, Rate, TagKv, TopK


def test_query_equality_compares_aggregator():
    left = Query(aggregator=Aggregator.SUM, metric="service.qps")
    right = Query(aggregator=Aggregator.AVG, metric="service.qps")

    assert left != right


def test_query_equality_ignores_group_and_filter_order():
    left = Query(
        aggregator=Aggregator.SUM,
        metric="service.qps",
        groups=[
            TagKv(key="host", values=["a", "b"], group_by=True),
            TagKv(key="cluster", values=["cn"], group_by=True),
        ],
        filters=[
            TagKv(key="env", values=["prod"]),
            TagKv(key="region", values=["cn"]),
        ],
    )
    right = Query(
        aggregator=Aggregator.SUM,
        metric="service.qps",
        groups=[
            TagKv(key="cluster", values=["cn"], group_by=True),
            TagKv(key="host", values=["b", "a"], group_by=True),
        ],
        filters=[
            TagKv(key="region", values=["cn"]),
            TagKv(key="env", values=["prod"]),
        ],
    )

    assert left == right


def test_tagkv_equality_keeps_group_by_semantics():
    group = TagKv(key="host", values=["a"], group_by=True)
    filter_ = TagKv(key="host", values=["a"], group_by=False)

    assert group != filter_


def test_multifield_equality_keeps_function_semantics():
    plain = MultiField(fields=["value", "weight"])
    weighted = MultiField(
        fields=["value", "weight"],
        field_func="weighted_avg",
        func_params={"value": "value", "weight": "weight"},
    )

    assert plain != weighted


def test_models_validate_assignment():
    downsampling = Downsampling(interval="1m", aggregator=Aggregator.AVG)

    with pytest.raises(ValidationError):
        downsampling.interval = "1"


def test_query_serializes_optional_components_in_order():
    query = Query(
        aggregator=Aggregator.MAX,
        downsampling=Downsampling(interval="5m", aggregator=Aggregator.AVG, fill_policy="zero"),
        rate=Rate(counter=True, delta=True, downsample="after_downsample"),
        topk=TopK(top_bottom="top", num=3, option="max"),
        tenant="tenant",
        metric="service.latency",
        groups=[TagKv(key="host", values=["b", "a"], group_by=True)],
        filters=[TagKv(key="env", values=["prod"], filter_type=FilterType.LITERAL_OR)],
        multifields=MultiField(fields=["rt.pct90", "count.rate"]),
    )

    assert str(query) == (
        "max:5m-avg-zero:rate{counter,,,diff,after_downsample}:top-3-max:"
        "[tenant]service.latency{host=literal_or(a|b)}{env=literal_or(prod)}[count.rate,rt.pct90]"
    )


def test_calc_interval_seconds_supports_compound_intervals():
    assert calc_interval_seconds("1d12h30m") == 131400
    assert calc_interval_seconds("1s500ms") == 1.5


def test_calc_interval_seconds_rejects_invalid_interval():
    with pytest.raises(ValueError, match="Illegal interval format"):
        calc_interval_seconds("1x")
