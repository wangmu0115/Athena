from athena_kit.matplotlib.styles.base import FontStyle

DEFAULT_FONT = FontStyle(
    family="sans-serif",
    fallbacks=[
        "Hiragino Sans GB",
        "Arial Unicode MS",
        "PingFang SC",
        "Noto Sans CJK SC",
        "Microsoft YaHei",
    ],
    size=10.0,
    weight="normal",
    color="#111111",
)
