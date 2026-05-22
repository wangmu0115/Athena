from pydantic import Field

from athena_charts_matplotlib.styles._base import _BaseStyle


class MatplotlibTickStyle(_BaseStyle):
    visible: bool | None = Field(None, description="是否显示刻度")
    


    label_visible: bool | None = Field(None, description="是否显示刻度标签")
    label_rotation: float | None = Field(0.0, ge=-90, le=90, description="刻度标签旋转角度")
    label_format: TickLabelFormat = Field(default_factory=TickLabelFormat, description="刻度格式化配置")
    locator: TickLocator = Field(default_factory=TickLocator, description="刻度位置配置")

    tick_color: str | None = Field(None, description="刻度线颜色")
    tick_width: float | None = Field(None, gt=0, description="刻度线宽度")
    tick_length: float | None = Field(None, gt=0, description="刻度线长度")
    tick_direction: TickDirection | None = Field(None, description="刻度线朝向")
    label_fontsize: int | None = Field(None, gt=0, description="刻度文本字号")
    label_fontweight: FontWeight | None = Field(None, description="刻度文本字体粗细")
    label_color: str | None = Field(None, description="刻度文本颜色")
    label_rotation: float | None = Field(None, ge=-90, le=90, description="刻度文本旋转角度")

    ## ***************************************************************************


## * TICKS                                                                   *
## ***************************************************************************
## See https://matplotlib.org/stable/api/axis_api.html#matplotlib.axis.Tick
# xtick.top:           False   # draw ticks on the top side
# xtick.bottom:        True    # draw ticks on the bottom side
# xtick.labeltop:      False   # draw label on the top
# xtick.labelbottom:   True    # draw label on the bottom
# xtick.major.size:    3.5     # major tick size in points
# xtick.minor.size:    2       # minor tick size in points
# xtick.major.width:   0.8     # major tick width in points
# xtick.minor.width:   0.6     # minor tick width in points
# xtick.major.pad:     3.5     # distance to major tick label in points
# xtick.minor.pad:     3.4     # distance to the minor tick label in points
# xtick.color:         black   # color of the ticks
# xtick.labelcolor:    inherit # color of the tick labels or inherit from xtick.color
# xtick.labelsize:     medium  # font size of the tick labels
# xtick.direction:     out     # direction: {in, out, inout}
# xtick.minor.visible: False   # visibility of minor ticks on x-axis
# xtick.major.top:     True    # draw x axis top major ticks
# xtick.major.bottom:  True    # draw x axis bottom major ticks
# xtick.minor.top:     True    # draw x axis top minor ticks
# xtick.minor.bottom:  True    # draw x axis bottom minor ticks
# xtick.minor.ndivs:   auto    # number of minor ticks between the major ticks on x-axis
# xtick.alignment:     center  # alignment of xticks

# ytick.left:          True    # draw ticks on the left side
# ytick.right:         False   # draw ticks on the right side
# ytick.labelleft:     True    # draw tick labels on the left side
# ytick.labelright:    False   # draw tick labels on the right side
# ytick.major.size:    3.5     # major tick size in points
# ytick.minor.size:    2       # minor tick size in points
# ytick.major.width:   0.8     # major tick width in points
# ytick.minor.width:   0.6     # minor tick width in points
# ytick.major.pad:     3.5     # distance to major tick label in points
# ytick.minor.pad:     3.4     # distance to the minor tick label in points
# ytick.color:         black   # color of the ticks
# ytick.labelcolor:    inherit # color of the tick labels or inherit from ytick.color
# ytick.labelsize:     medium  # font size of the tick labels
# ytick.direction:     out     # direction: {in, out, inout}
# ytick.minor.visible: False   # visibility of minor ticks on y-axis
# ytick.major.left:    True    # draw y axis left major ticks
# ytick.major.right:   True    # draw y axis right major ticks
# ytick.minor.left:    True    # draw y axis left minor ticks
# ytick.minor.right:   True    # draw y axis right minor ticks
# ytick.minor.ndivs:   auto    # number of minor ticks between the major ticks on y-axis
# ytick.alignment:     center_baseline  # alignment of yticks
