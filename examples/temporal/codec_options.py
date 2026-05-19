from athena_core.temporal.codec import DateTimeCodec, DateTimeCodecOptions

codec = DateTimeCodec(
    DateTimeCodecOptions(
        output_format="iso",
        timestamp_unit="ms",
        naive_datetime_policy="assume_timezone",
    )
)

dt = codec.parse("2026-05-19 12:30:00", timezone="Asia/Shanghai")
value = codec.format(dt)

print(dt)
print(value)
