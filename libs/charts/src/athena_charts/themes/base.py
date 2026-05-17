from pydantic import Field

from athena_core.models import BaseAthenaModel


class TextTheme(BaseAthenaModel):
    color: str = Field(..., description="默认文本颜色")
    font_family: str = Field(..., description="默认字体族")
    sans_serif_fonts: list[str] = Field(default_factory=list)


class PaletteTheme(BaseAthenaModel):
    colors: list[str] = Field(default_factory=list, description="默认颜色调色板")


class FigureTheme(BaseAthenaModel):
    width: int | None = Field(None, gt=0, description="画布宽度，单位 px")
    height: int | None = Field(None, gt=0, description="画布高度，单位 px")
    background_color: str | None = Field(None, description="画布背景颜色")
    edge_color: str | None = Field(None, description="画布边框颜色")
    title_font_size: int | None = Field(None, gt=0, description="画布标题字号")
    subtitle_font_size: int | None = Field(None, gt=0, description="画布副标题字号")


class ChartTheme(BaseAthenaModel):
    background_color: str | None = Field(None, description="图表区域背景颜色")
    title_font_size: int | None = Field(None, gt=0, description="图表标题字号")
    subtitle_font_size: int | None = Field(None, gt=0, description="图表副标题字号")


class AxisTheme(BaseAthenaModel):
    edge_color: str | None = Field(None, description="轴线默认颜色")
    label_color: str | None = Field(None, description="标签文本颜色")
    label_font_size: int | None = Field(None, gt=0, description="标签字号")
    tick_color: str | None = Field(None, description="刻度线默认颜色")
    tick_font_size: int | None = Field(None, gt=0, description="刻度标签字号")


class GridTheme(BaseAthenaModel):
    visible: bool | None = Field(None, description="是否显示网格线")
    color: str | None = Field(None, description="网格线颜色")
    alpha: float | None = Field(None, ge=0, le=1, description="网格线透明度")
    line_width: float | None = Field(None, gt=0, description="网格线宽度")


class LegendTheme(BaseAthenaModel):
    visible: bool | None = Field(None, description="是否显示图例")
    title_font_size: int | None = Field(None, gt=0, description="图例标题字号")
    font_size: int | None = Field(None, gt=0, description="图例文本字号")


class PlotTheme(BaseAthenaModel):
    opacity: float | None = Field(None, ge=0, le=1, description="默认透明度")
    line_width: float | None = Field(None, gt=0, description="默认线宽")
    marker_size: float | None = Field(None, gt=0, description="默认标记大小")
    bar_width: float | None = Field(None, gt=0, le=1, description="默认柱宽")


class Theme(BaseAthenaModel):
    text: TextTheme = Field(default_factory=TextTheme, description="全局文本主题")
    palette: PaletteTheme = Field(default_factory=PaletteTheme, description="调色板主题")
    figure: FigureTheme = Field(default_factory=FigureTheme, description="画布主题")
    chart: ChartTheme = Field(default_factory=ChartTheme, description="图表主题")
    axis: AxisTheme = Field(default_factory=AxisTheme, description="坐标轴主题")
    grid: GridTheme = Field(default_factory=GridTheme, description="网格主题")
    legend: LegendTheme = Field(default_factory=LegendTheme, description="图例主题")
    plot: PlotTheme = Field(default_factory=PlotTheme, description="图层主题")

    def pick_color(self, index: int) -> str | None:
        if self.palette and self.palette.colors:
            return self.palette.colors[index % len(self.palette.colors)]
        return None
