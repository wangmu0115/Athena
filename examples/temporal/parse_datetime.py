from athena_core.temporal.codec import parse_datetime

# dt = parse_datetime("2026-05-01 12:30:25", "Asia/Shanghai")
dt = parse_datetime("2026-05-01 12:30:25")

print(dt)
print(dt.tzinfo)
