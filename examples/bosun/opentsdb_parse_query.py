from athena_kit.bosun.opentsdb.parser import parse_query

query = parse_query(
    "sum:1m-avg:rate{counter,,,diff,after_downsample}:top-10-max:"
    "[tenant]service.latency{host=a|b}{env=prod}[rt.pct90,count.rate]"
)

print(query)
print(query.metric)
print(query.groups)
print(query.filters)
print(query.multifields)
