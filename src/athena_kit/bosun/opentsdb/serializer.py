from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from athena_kit.bosun.opentsdb.models import (
        Downsampling,
        MultiField,
        Query,
        Rate,
        TagKv,
        TopK,
    )


def serialize_downsampling(downsampling: Downsampling) -> str:
    """将降采样配置序列化为查询字符串片段。

    输出格式固定为 `interval-aggregator-fill_policy`，例如 `1m-avg-none`。
    该函数只负责结构化模型到字符串的转换，不重复执行字段合法性校验。
    """
    return f"{downsampling.interval}-{downsampling.aggregator}-{downsampling.fill_policy}"


def serialize_rate(rate: Rate) -> str:
    """将 rate 或 diff 配置序列化为查询字符串片段。

    输出格式遵循 OpenTSDB/Bosun 的 `rate{counter,,,diff,downsample}` 表达方式。
    未启用的选项会保留为空位，保证序列化结果可以被 parser 按相同字段位置解析回结构化模型。
    """
    counter = "counter" if rate.counter else ""
    delta = "diff" if rate.delta else ""
    return f"rate{{{counter},,,{delta},{rate.downsample}}}"


def serialize_topk(topk: TopK) -> str:
    """将 TopK 配置序列化为查询字符串片段。

    输出格式固定为 `top|bottom-num-option`，例如 `top-10-max`。
    数量范围和 option 合法性由模型层负责，该函数只保留字符串拼接规则。
    """
    return f"{topk.top_bottom}-{topk.num}-{topk.option}"


def serialize_tagkv(tagkv: TagKv) -> str:
    """将 Tag 条件序列化为查询字符串片段。

    输出格式为 `tagk=filter_type(tagv1|tagv2)`。Tag values 会先排序再拼接，使同一组 value 在不同输入顺序下
    得到稳定的字符串表示，便于比较、去重和测试断言。
    """
    return f"{tagkv.key}={tagkv.filter_type}({'|'.join(sorted(tagkv.values))})"


def serialize_multifield(multifield: MultiField) -> str:
    """将多值字段配置序列化为查询字符串片段。

    普通字段列表输出为逗号分隔形式，例如 `count.rate,rt.pct90`，函数字段输出为 `func(param=value,...)`。
    函数参数按照参数名排序，保证结构相同的配置拥有稳定的字符串表达。
    """
    if multifield.field_func is None:
        return ",".join(sorted(multifield.fields))
    params = ",".join(f"{name}={multifield.func_params[name]}" for name in sorted(multifield.func_params))
    return f"{multifield.field_func}({params})"


def serialize_query(query: Query) -> str:
    """将完整 OpenTSDB 查询模型序列化为查询字符串。

    输出格式按 `aggregator[:downsampling][:rate][:topk]:[tenant]metric` 的顺序拼接，并始终输出 group 与 filter 两段
    花括号，即使二者为空也会保留 `{}{}`。这种规范化输出便于 round-trip 解析和 query equality 的稳定判断。
    """
    query_string = str(query.aggregator)
    if query.downsampling is not None:
        query_string += f":{serialize_downsampling(query.downsampling)}"
    if query.rate is not None:
        query_string += f":{serialize_rate(query.rate)}"
    if query.topk is not None:
        query_string += f":{serialize_topk(query.topk)}"

    query_string += f":[{query.tenant or 'default'}]{query.metric}"
    query_string += "{" + ",".join(serialize_tagkv(group_) for group_ in query.groups) + "}"
    query_string += "{" + ",".join(serialize_tagkv(filter_) for filter_ in query.filters) + "}"

    if query.multifields is not None:
        query_string += f"[{serialize_multifield(query.multifields)}]"

    return query_string
