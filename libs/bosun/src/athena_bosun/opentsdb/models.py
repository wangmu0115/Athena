from __future__ import annotations

from collections import Counter
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from athena_bosun.opentsdb.enums import Aggregator, FilterType, MultiFunction
from athena_bosun.opentsdb.serializer import (
    serialize_downsampling,
    serialize_multifield,
    serialize_query,
    serialize_rate,
    serialize_tagkv,
    serialize_topk,
)


class _BaseOpenTSDBModel(BaseModel):
    """OpenTSDB 模块内部使用的 Pydantic 模型基类。

    该基类只服务于 `opentsdb` 层，不作为公共 API 导出。
    它统一约束未知字段、赋值校验和字符串空白处理，避免各个模型重复声明同一组 Pydantic 配置。
    """

    model_config = ConfigDict(
        extra="forbid",  # 禁止未知字段
        arbitrary_types_allowed=True,  # 允许自定义对象
        populate_by_name=True,  # alias 与 field_name 双支持
        validate_assignment=True,  # 修改字段重新校验
        str_strip_whitespace=True,  # 自动 trim
    )


class Downsampling(_BaseOpenTSDBModel):
    """OpenTSDB 降采样配置。

    表示查询中的 `interval-aggregator-fill_policy` 片段，例如 `1m-avg-none`。
    `interval` 保存降采样窗口，`aggregator` 保存窗口内聚合方式，`fill_policy` 保存空值填充策略。
    """

    interval: str = Field(..., description="降采样时间间隔，例如 1m30s", pattern=r"^(\d+(?:ms|[smhdwny]))+$")
    aggregator: Aggregator = Field(..., description="降采样聚合方式")
    fill_policy: Literal["none", "nan", "null", "zero", "int"] = Field("none", description="空值填充策略")

    def to_query_string(self) -> str:
        """序列化为 OpenTSDB 降采样查询片段。"""
        return serialize_downsampling(self)

    def __str__(self) -> str:
        return self.to_query_string()


class Rate(_BaseOpenTSDBModel):
    """OpenTSDB rate 或 diff 配置。

    表示查询中的 `rate{...}` 片段。
    `counter` 控制是否按 counter 语义处理非负变化量，`delta` 控制
    是否使用相邻点差值，`downsample` 控制 rate 与 downsampling 的
    计算顺序。
    """

    counter: bool = Field(..., description="是否仅保留非负值的计算结果")
    delta: bool = Field(..., description="是否使用两个点的差值")
    downsample: Literal["before_downsample", "after_downsample"] = Field(
        "before_downsample",
        description="计算 rate 的先后顺序",
    )

    def to_query_string(self) -> str:
        """序列化为 OpenTSDB rate 查询片段。"""
        return serialize_rate(self)

    def __str__(self) -> str:
        return self.to_query_string()


class TopK(_BaseOpenTSDBModel):
    """OpenTSDB TopK 配置。

    表示查询中的 `top|bottom-num-option` 片段，例如 `top-10-max`。
    `top_bottom` 决定取最大还是最小的一组时序，`num` 决定保留数量，`option` 决定排序时使用的聚合方式。
    """

    top_bottom: Literal["top", "bottom"] = Field("top", description="从上往下或者从下往上获取 K 个结果")
    num: int = Field(10, description="返回结果的数量", ge=1, le=65536)
    option: Literal["max", "min", "avg", "sum", "count"] = Field(..., description="使用排序的时序聚合方式")

    def to_query_string(self) -> str:
        """序列化为 OpenTSDB TopK 查询片段。"""
        return serialize_topk(self)

    def __str__(self) -> str:
        return self.to_query_string()


class TagKv(_BaseOpenTSDBModel):
    """OpenTSDB Tag 条件。

    表示 group 或 filter 段中的单个 Tag 条件。
    `key` 是 tag key，`values` 是候选 tag values，`filter_type` 是过滤函数，`group_by` 用于区分该条件是否来自 group 段。
    相等性比较会忽略 values 的顺序，但会保留重复值的计数语义。
    """

    key: str = Field(..., description="Tag Key", min_length=1)
    values: list[str] = Field(..., description="Tag Values", min_length=1)
    filter_type: FilterType = Field(FilterType.LITERAL_OR, description="Tag Values 的过滤函数")
    group_by: bool = Field(False, description="是否按照 Tag Values 分组")

    def to_query_string(self) -> str:
        """序列化为 OpenTSDB Tag 查询片段。"""
        return serialize_tagkv(self)

    def __str__(self) -> str:
        return self.to_query_string()

    def __hash__(self) -> int:
        return hash((self.key, self.filter_type, self.group_by, tuple(sorted(Counter(self.values).items()))))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TagKv):
            return NotImplemented
        return (
            self.key == other.key
            and self.filter_type == other.filter_type
            and self.group_by == other.group_by
            and Counter(self.values) == Counter(other.values)
        )


class MultiField(_BaseOpenTSDBModel):
    """OpenTSDB 多值字段配置。

    表示 metric 后缀中的 `[multiFieldExpr]`。
    普通多字段查询使用 `fields` 保存字段名列表；函数式多字段查询额外
    使用 `field_func` 和 `func_params` 保存函数名与参数映射。
    相等性比较会忽略普通字段顺序，但不会忽略函数名和函数参数。
    """

    fields: list[str] = Field(..., description="多值字段名称", min_length=1)
    field_func: MultiFunction | None = Field(None, description="多值函数")
    func_params: dict[str, str] = Field(default_factory=dict, description="多值函数的参数")

    def to_query_string(self) -> str:
        """序列化为 OpenTSDB 多值字段查询片段。"""
        return serialize_multifield(self)

    def __str__(self) -> str:
        return self.to_query_string()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, MultiField):
            return NotImplemented
        return (
            Counter(self.fields) == Counter(other.fields)
            and self.field_func == other.field_func
            and self.func_params == other.func_params
        )


class Query(_BaseOpenTSDBModel):
    """完整 OpenTSDB 查询结构。

    该模型组合聚合方式、可选降采样、可选 rate、可选 TopK、租户、指标名、group/filter Tag 条件和多值字段配置。
    `groups` 与 `filters` 使用列表保存，但相等性比较会忽略列表顺序，以表达查询条件集合的语义。
    """

    aggregator: Aggregator = Field(Aggregator.SUM, description="聚合方式")
    downsampling: Downsampling | None = Field(None, description="降采样配置")
    rate: Rate | None = Field(None, description="对结果求导或者求差值")
    topk: TopK | None = Field(None, description="排序获取最多 K 个结果")
    tenant: str = Field("default", description="租户", min_length=1)
    metric: str = Field(..., description="指标名称", min_length=1)
    groups: list[TagKv] = Field(default_factory=list, description="分组条件 Tag 列表")
    filters: list[TagKv] = Field(default_factory=list, description="过滤条件 Tag 列表")
    multifields: MultiField | None = Field(None, description="多值配置")

    @classmethod
    def parse_query(cls, query_string: str) -> Query:
        """从 OpenTSDB 查询字符串解析并构造 `Query`。"""
        from athena_bosun.opentsdb.parser import parse_query

        return parse_query(query_string)

    def to_query_string(self) -> str:
        """序列化为规范化 OpenTSDB 查询字符串。"""
        return serialize_query(self)

    def __str__(self) -> str:
        return self.to_query_string()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Query):
            return NotImplemented
        return (
            self.aggregator == other.aggregator
            and self.tenant == other.tenant
            and self.metric == other.metric
            and self.downsampling == other.downsampling
            and self.rate == other.rate
            and self.topk == other.topk
            and Counter(self.groups) == Counter(other.groups)
            and Counter(self.filters) == Counter(other.filters)
            and self.multifields == other.multifields
        )
