from pydantic import BaseModel, Field


class FigureTheme(BaseModel):
    font_family: str = Field("sans-serif", description="图表默认字体族")
    sans_serif_fonts: list[str] = Field(
        default_factory=lambda: [
            "Hiragino Sans GB",
            "Arial Unicode MS",
            "PingFang SC",
            "Noto Sans CJK SC",
            "Microsoft YaHei",
            "SimHei",
            "DejaVu Sans",
            "sans-serif",
        ]
    )

    text_color: str = Field("#111111", description="默认文本颜色")
    title_fontsize: int = Field(13, gt=0, description="图表标题字号")
    subtitle_fontsize: int = Field(11, gt=0, description="图表副标题字号")

    figure__background_color: str = Field("white", description="图表画布背景颜色")

    axes__background_color: str = Field("white", description="绘图区背景颜色")
    axes__edge_color: str = Field("#333333", description="轴线默认颜色")
    axes__label_color: str = Field("#111111", description="标签文本颜色")
    axes__label_fontsize: int = Field(10, gt=0, description="坐标轴标签字号")

    axis__tick_fontsize: int = Field(8, gt=0, description="刻度标签字号")
    axis__tick_color: str = Field("#333333", description="刻度线的默认颜色")

    grid__color: str = Field("#999999", description="网格线颜色")
    grid__alpha: float = Field(0.3, ge=0, le=1, description="网格线透明度")
    grid__linestyle: str = Field("--", description="网格线样式")
    grid__linewidth: float = Field(0.5, gt=0, description="网格线宽度")

    legend__title_fontsize: int = Field(10, gt=0, description="图例标题字号")
    legend__fontsize: int = Field(8, gt=0, description="图例文本字号")

    color_palette: list[str] = Field(
        default_factory=lambda: [
            "#1f77b4",
            "#ff7f0e",
            "#2ca02c",
            "#d62728",
            "#9467bd",
            "#8c564b",
            "#e377c2",
            "#7f7f7f",
            "#bcbd22",
            "#17becf",
        ],
        description="默认颜色调色板",
    )

    def pick_color(self, index: int) -> str | None:
        """从调色板中选取颜色"""

        if not self.color_palette:
            return None
        return self.color_palette[index % len(self.color_palette)]
