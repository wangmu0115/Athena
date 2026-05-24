from typing import Literal

type BarLayoutMode = Literal["group", "stack", "overlay"]
"""柱状图布局模式定义，用于控制多个 BarPlot 在同一坐标系中的排列方式。

取值说明：
    - group: 分组模式。多个柱状图会按照类别并排显示，每个系列在同一分类下占据独立的位置，适用于对比不同系列之间的数值差异。
    - stack: 堆叠模式。多个柱状图会在同一分类位置按数值方向累积堆叠，后一个系列会以上一个系列的终点作为起始位置。
    - overlay: 覆盖模式。多个柱状图绘制在同一位置，相互覆盖，后绘制的柱子会覆盖先绘制的柱子。
"""
