from datetime import datetime
from zoneinfo import ZoneInfo

from athena_core.temporal.codec import format_datetime

dt = datetime(2026, 5, 19, 12, 30, tzinfo=ZoneInfo("Asia/Shanghai"))

print(format_datetime(dt, output_format="formatted"))
print(format_datetime(dt, output_format="iso"))
print(format_datetime(dt, output_format="timestamp_ms"))
