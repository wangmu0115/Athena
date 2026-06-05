from athena_kit.core.temporal.codec import parse_datetime
from athena_kit.core.temporal.timezone import get_timezone, timezone_context

print(get_timezone())

with timezone_context("Asia/Tokyo"):
    print(get_timezone())
    print(parse_datetime("2026-05-19 12:30:00"))

print(get_timezone())
