from pydantic import BaseModel, Field


class FigureTheme(BaseModel):
    font_family: str = Field("sans-serif", description="图表默认字体族，例如 sans-serif, serif, monospace 等")
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
        ],
        description="sans-serif 字体候选列表，按顺序用于中文与 Unicode 字体回退",
    )

    title_fontsize: int = Field(13, description="图表标题字号", gt=0)
    subtitle_fontsize: int = Field(11, description="图表副标题字号", gt=0)

    label_fontsize: int = Field(10, description="坐标轴标签字号", gt=0)
    tick_label_fontsize: int = Field(8, description="坐标轴刻度标签字号", gt=0)

    legend_title_fontsize: int = Field(10, description="图例标题字号", gt=0)
    legend_fontsize: int = Field(8, description="图例文本字号", gt=0)

    background_color: str = Field("white", description="图表画布背景颜色")
    axes_background_color: str = Field("white", description="绘图区背景颜色")

    text_color: str = Field("#111111", description="默认文本颜色")
    axis_color: str = Field("#333333", description="坐标轴、刻度线的默认颜色")

    grid_color: str = Field("#999999", description="网格线颜色")
    grid_alpha: float = Field(0.3, description="网格线透明度", ge=0, le=1)
    grid_linestyle: str = Field("--", description="网格线样式")
    grid_linewidth: float = Field(0.5, description="网格线宽度", gt=0)

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
        description="数据系列默认颜色调色板",
    )

    def pick_color_from_palette(self, index: int) -> str | None:
        if not self.color_palette:
            return None
        return self.color_palette[index % len(self.color_palette)]
