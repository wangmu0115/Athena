from typing import Literal

# Unix 时间戳精度单位：
# - s: 秒级时间戳
# - ms: 毫秒级时间戳
type TimestampUnit = Literal["s", "ms"]

# 日期时间边界补全策略：
# - start: 当天开始时间 `time.min`
# - end: 当天结束时间 `time.max`
# - noon: 当天中午时间 `time(hour=12, minute=0, second=0)`
type DateBoundaryPolicy = Literal["start", "end", "noon"]

# naive datetime 处理策略：
# - assume_timezone: 将 naive datetime 视为属于当前有效时区
# - raise: 遇到 naive datetime 时抛出异常
type NaiveDateTimeHandling = Literal["assume_timezone", "raise"]

# 时间输出格式：
# - native: 返回 `datetime.time` 原生对象
# - iso: 返回 `time.isoformat()` 生成的 ISO 格式字符串
# - formatted: 返回按 `format_pattern` 格式化后的字符串
type TimeOutputFormat = Literal["native", "iso", "formatted"]

# 日期输出格式：
# - native: 返回 `datetime.date` 原生对象
# - iso: 返回 `date.isoformat()` 生成的 ISO 格式字符串
# - formatted: 返回按 `format_pattern` 格式化后的字符串
# - datetime: 返回补全时间边界后的 `datetime.datetime`
# - timestamp_s: 返回 Unix 秒级时间戳
# - timestamp_ms: 返回 Unix 毫秒级时间戳
type DateOutputFormat = Literal["native", "iso", "formatted", "datetime", "timestamp_s", "timestamp_ms"]

# 日期时间输出格式：
# - native: 返回 `datetime.datetime` 原生对象
# - iso: 返回 `datetime.isoformat()` 生成的 ISO 格式字符串
# - rfc5322: 返回 RFC 5322 格式字符串
# - formatted: 返回按 `format_pattern` 格式化后的字符串
# - timestamp_s: 返回 Unix 秒级时间戳
# - timestamp_ms: 返回 Unix 毫秒级时间戳
type DateTimeOutputFormat = Literal["native", "iso", "rfc5322", "formatted", "timestamp_s", "timestamp_ms"]
