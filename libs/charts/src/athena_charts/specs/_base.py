from pydantic import BaseModel, ConfigDict


class _BaseSpec(BaseModel):
    """声明式图表规范基类，该类仅供 `athena_charts.specs` 内部复用，不作为稳定公共 API 导出。

    Specs 用于描述绘图各层抽象的声明式规范，例如 FigureSpec、ChartSpec、CoordSpec、AxisSpec、PlotSpec 等。
    """

    model_config = ConfigDict(
        extra="forbid",                # 禁止未知字段
        arbitrary_types_allowed=True,  # 允许自定义对象
        validate_assignment=True,      # 修改字段重新校验
        str_strip_whitespace=True,     # 自动 trim
    )  # fmt: off
