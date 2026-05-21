from pydantic import BaseModel, ConfigDict, Field

from athena_charts.specs.rules import DataField


class DataPointContext(BaseModel):
    """单个数据点的运行时上下文。

    用于在 transform 阶段为条件判断、动态样式解析、数据标签格式化等逻辑提供统一的数据访问入口。
    该对象不是声明式 spec，而是渲染前计算过程中产生或传递的运行时上下文。
    """

    # 禁止未知字段, 允许自定义对象, 自动 trim
    model_config = ConfigDict(extra="forbid", arbitrary_types_allowed=True, str_strip_whitespace=True)

    x: object | None = Field(None, description="当前数据点的 X 值")
    y: object | None = Field(None, description="当前数据点的 Y 值")
    category: str | None = Field(None, description="当前数据点的分类值")
    value: object | None = Field(None, description="当前数据点的原始值或主值")
    name: str | None = Field(None, description="当前数据点名称")
    index: int | None = Field(None, ge=0, description="当前数据点索引")
    plot_name: str | None = Field(None, description="当前数据点所属图层名称")

    def get(self, field: DataField) -> object | None:
        """根据字段名获取数据点上下文值。"""
        match field:
            case "x":
                return self.x
            case "y":
                return self.y
            case "category":
                return self.category
            case "value":
                return self.value
            case "name":
                return self.name
            case "index":
                return self.index
            case "plot_name":
                return self.plot_name
            case _:
                raise ValueError(f"Unsupported data context field: {field}.")
