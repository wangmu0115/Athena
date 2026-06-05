from typing import Literal

type TimestampUnit = Literal["s", "ms"]
"""Unix 时间戳精度单位。

取值说明：
    - s: 秒级时间戳，符合 Python `datetime.timestamp()` 的默认语义。
    - ms: 毫秒级时间戳，常见于前端、日志平台和部分外部 API。
"""


type DateBoundaryPolicy = Literal["start", "end", "end_max", "noon"]
"""日期补全为日期时间时使用的时间边界策略。

取值说明：
    - start: 补全为当天开始时间，即 `00:00:00`。
    - `end`：补全为当天秒级结束时间，即 `23:59:59`。
    - `end_max`：补全为 Python 最大时间，即 `23:59:59.999999`。
    - `noon`：补全为当天中午时间，即 `12:00:00`。
"""


type NaiveDateTimePolicy = Literal["assume_timezone", "raise"]
"""不带时区信息的原生 `datetime` 输入处理策略。

该策略只作用于用户直接传入的 Python `datetime` 对象，不作用于字符串解析结果。
字符串如果不包含时区信息，会被视为目标时区下的本地时间。
"""


type TimeOutputFormat = Literal["native", "iso", "formatted"]
"""时间输出格式。

取值说明：
    - native: 返回 `datetime.time` 原生对象
    - iso: 返回 `time.isoformat()` 生成的 ISO 格式字符串
    - formatted: 返回按 `format_pattern` 格式化后的字符串
"""


type DateOutputFormat = Literal["native", "iso", "formatted", "datetime", "timestamp_s", "timestamp_ms"]
"""日期输出格式。

取值说明：
    - native: 返回 `datetime.date` 原生对象
    - iso: 返回 `date.isoformat()` 生成的 ISO 格式字符串
    - formatted: 返回按 `format_pattern` 格式化后的字符串
    - datetime: 返回补全时间边界后的 `datetime.datetime`
    - timestamp_s: 返回 Unix 秒级时间戳
    - timestamp_ms: 返回 Unix 毫秒级时间戳
"""


type DateTimeOutputFormat = Literal["native", "iso", "rfc5322", "formatted", "timestamp_s", "timestamp_ms"]
"""日期时间输出格式。

取值说明：
    - native: 返回 `datetime.datetime` 原生对象
    - iso: 返回 `datetime.isoformat()` 生成的 ISO 格式字符串
    - rfc5322: 返回 RFC 5322 格式字符串
    - formatted: 返回按 `format_pattern` 格式化后的字符串
    - timestamp_s: 返回 Unix 秒级时间戳
    - timestamp_ms: 返回 Unix 毫秒级时间戳
"""
