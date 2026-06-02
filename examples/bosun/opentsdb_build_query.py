from athena_bosun.opentsdb.enums import Aggregator, FilterType
from athena_bosun.opentsdb.models import Downsampling, MultiField, Query, Rate, TagKv, TopK

query = Query(
    aggregator=Aggregator.MAX,
    downsampling=Downsampling(interval="5m", aggregator=Aggregator.AVG, fill_policy="zero"),
    rate=Rate(counter=True, delta=True, downsample="after_downsample"),
    topk=TopK(top_bottom="top", num=3, option="max"),
    tenant="tenant",
    metric="service.latency",
    groups=[
        TagKv(key="host", values=["b", "a"], group_by=True),
    ],
    filters=[
        TagKv(key="env", values=["prod"], filter_type=FilterType.LITERAL_OR),
    ],
    multifields=MultiField(fields=["rt.pct90", "count.rate"]),
)

print(query.to_query_string())
