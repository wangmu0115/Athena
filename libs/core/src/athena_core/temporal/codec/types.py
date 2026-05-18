from typing import Literal

type TimestampUnit = Literal["s", "ms"]


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
