from typing import Literal

type TimestampUnit = Literal["s", "ms"]

type NaiveDateTimePolicy = Literal["assume_local", "raise"]
type DateBoundaryPolicy = Literal["start", "end", "noon"]

DateTimeDecodeTarget = Literal[
    "datetime",
    "string",
    "iso",
    "timestamp_s",
    "timestamp_ms",
]

DateDecodeTarget = Literal[
    "date",
    "string",
    "iso",
]

TimeDecodeTarget = Literal[
    "time",
    "string",
    "iso",
]
