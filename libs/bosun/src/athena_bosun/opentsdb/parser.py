import re
from collections.abc import Callable

from pydantic import ValidationError

from athena_bosun.opentsdb.enums import FilterType
from athena_bosun.opentsdb.exceptions import OpenTSDBParseError
from athena_bosun.opentsdb.models import (
    Downsampling,
    MultiField,
    Query,
    Rate,
    TagKv,
    TopK,
)


def _build_model[ModelT](factory: Callable[[], ModelT], source: str) -> ModelT:
    """构造 OpenTSDB 模型并统一转换校验异常。

    parser 负责识别字符串结构，模型负责字段级合法性校验。该辅助函数用于把 Pydantic 的 `ValidationError`
    包装成 `OpenTSDBParseError`，让调用方只需要处理一种解析异常。
    """
    try:
        return factory()
    except ValidationError as exc:
        raise OpenTSDBParseError(f"Illegal OpenTSDB component: `{source}`.") from exc


def parse_downsampling(downsampling_string: str) -> Downsampling | None:
    """解析 OpenTSDB 降采样字符串。

    - 支持 `interval-aggregator` 和 `interval-aggregator-fill_policy` 两种形式，例如 `1m-avg`、`1m-avg-none`。
    - 当输入不像降采样片段时返回 `None`，便于完整 query parser 继续尝试后续组件。
    - 当输入看起来是降采样片段但字段数量或字段值非法时抛出 `OpenTSDBParseError`。
    """
    interval_pattern = re.compile(r"^(\d+(?:ms|[smhdwny]))+$")
    components = downsampling_string.split("-")

    match components:
        case [interval, aggregator, fill_policy] if interval_pattern.fullmatch(interval):
            return _build_model(
                lambda: Downsampling(interval=interval, aggregator=aggregator, fill_policy=fill_policy),
                downsampling_string,
            )
        case [interval, aggregator] if interval_pattern.fullmatch(interval):
            return _build_model(
                lambda: Downsampling(interval=interval, aggregator=aggregator),
                downsampling_string,
            )
        case [interval, *_] if interval_pattern.fullmatch(interval):
            raise OpenTSDBParseError(f"Illegal downsampling string: `{downsampling_string}`.")
        case _:
            return None


def parse_rate(rate_string: str) -> Rate | None:
    """解析 OpenTSDB rate 或 diff 字符串。

    - 支持 `rate`、`rate{}`、`rate{counter}`，以及完整字段位格式 `rate{counter,,,diff,before_downsample}`。
    - 完整格式中的空字段位表示未启用对应选项，空 downsample 会回退为 `before_downsample`。
    - 当输入不是 rate 片段时返回 `None`。
    - 当以 rate 开头但结构非法时抛出 `OpenTSDBParseError`。
    """
    if re.fullmatch(r"rate|rate\{\s*\}", rate_string):
        return Rate(counter=False, delta=False)
    if not rate_string.startswith("rate"):
        return None
    if not rate_string.startswith("rate{") or not rate_string.endswith("}"):
        raise OpenTSDBParseError(f"Illegal rate string: `{rate_string}`.")

    components = [component.strip() for component in rate_string[5:-1].split(",")]
    match components:
        case ["counter"]:
            return Rate(counter=True, delta=False)
        case [
            "counter" | "" as counter,
            "",
            "",
            "diff" | "" as delta,
            "" | "before_downsample" | "after_downsample" as downsample,
        ]:
            return Rate(counter=bool(counter), delta=bool(delta), downsample=downsample or "before_downsample")
        case _:
            raise OpenTSDBParseError(f"Illegal rate string: `{rate_string}`.")


def parse_topk(topk_string: str) -> TopK | None:
    """解析 OpenTSDB TopK 字符串。

    - 支持 `top|bottom-num-option` 格式，例如 `top-10-max`。
    - 当输入不是 TopK 片段时返回 `None`，便于完整 query parser 把它交给后续组件。
    - 当输入以 `top` 或 `bottom` 开头但字段数量、数量值或 option 非法时抛出 `OpenTSDBParseError`。
    """
    components = topk_string.split("-")
    match components:
        case ["top" | "bottom" as top_bottom, num_str, option]:
            try:
                num = int(num_str)
            except ValueError as exc:
                raise OpenTSDBParseError(f"Illegal topk string: `{topk_string}`.") from exc
            return _build_model(
                lambda: TopK(top_bottom=top_bottom, num=num, option=option),
                topk_string,
            )
        case ["top" | "bottom", *_]:
            raise OpenTSDBParseError(f"Illegal topk string: `{topk_string}`.")
        case _:
            return None


def parse_tagkv(tagkv_string: str, group_by: bool = False) -> TagKv:
    """解析 OpenTSDB Tag 条件字符串。

    - 支持 `tagk=tagv1|tagv2` 和 `tagk=filter_type(tagv1|tagv2)` 两种形式。
    - 未显式指定过滤函数时默认使用 `literal_or`。
    - 多个 tag value 使用 `|` 分隔并会去除首尾空白。
    - `group_by` 用于标记该 Tag 条件来自 group 段还是 filter 段。
    """
    assign_index = tagkv_string.find("=")
    if assign_index == -1:
        raise OpenTSDBParseError(f"Illegal tagkv string: `{tagkv_string}`.")

    key = tagkv_string[:assign_index].strip()
    tag_value = tagkv_string[assign_index + 1 :].strip()
    filter_type_index = tag_value.find("(")
    if filter_type_index == -1:
        filter_type = FilterType.LITERAL_OR
    else:
        if not tag_value.endswith(")"):
            raise OpenTSDBParseError(f"Illegal tagkv string: `{tagkv_string}`.")
        filter_type = tag_value[:filter_type_index].strip()
        tag_value = tag_value[filter_type_index + 1 : -1]

    values = [value.strip() for value in tag_value.split("|") if value.strip()]
    return _build_model(lambda: TagKv(key=key, values=values, filter_type=filter_type, group_by=group_by), tagkv_string)


def parse_multifield(multi_string: str) -> MultiField:
    """解析 OpenTSDB 多值字段字符串。

    - 支持普通字段列表和函数式字段两种形式：
        - 普通字段列表使用逗号分隔，例如 `count.rate,rt.pct90`。
        - 函数式字段使用 `func(param=value,...)` 格式，例如 `weighted_avg(value=rt.pct90,weight=count)`。
    - 函数参数会解析为结构化字典，同时参数值会作为参与计算的字段列表。
    """
    callable_index = multi_string.find("(")
    if callable_index == -1:
        fields = [field.strip() for field in multi_string.split(",") if field.strip()]
        return _build_model(lambda: MultiField(fields=fields), multi_string)
    if not multi_string.endswith(")"):
        raise OpenTSDBParseError(f"Illegal multifield string: `{multi_string}`.")

    func = multi_string[:callable_index].strip()
    raw_params = [param.strip() for param in multi_string[callable_index + 1 : -1].split(",") if param.strip()]
    func_params: dict[str, str] = {}
    for raw_param in raw_params:
        param_name, separator, param_value = raw_param.partition("=")
        if separator == "" or not param_name.strip() or not param_value.strip():
            raise OpenTSDBParseError(f"Illegal multifield string: `{multi_string}`.")
        func_params[param_name.strip()] = param_value.strip()

    fields = list(func_params.values())
    return _build_model(lambda: MultiField(fields=fields, field_func=func, func_params=func_params), multi_string)


def parse_query(query_string: str) -> Query:
    """解析完整 OpenTSDB 查询字符串。

    - 解析顺序为 aggregator、可选 downsampling、可选 store、可选 rate、可选 topk，
    - 最后解析 metric、group tags、filter tags 和 multifields。
    - metric 未显式指定 tenant 时默认使用 `default`。
    - 该函数先收集所有解析结果，最后一次性构造 `Query`，避免在半解析状态下修改模型字段。
    """
    if not query_string.strip():
        raise OpenTSDBParseError("Illegal query string: query string is empty.")

    query_components = query_string.split(":")
    component_index = 0
    aggregator = query_components[component_index].strip()
    component_index += 1

    downsampling = None
    if component_index < len(query_components):
        downsampling = parse_downsampling(query_components[component_index].strip())
        if downsampling is not None:
            component_index += 1

    if component_index < len(query_components) and query_components[component_index].strip() == "store":
        component_index += 1

    rate = None
    if component_index < len(query_components):
        rate = parse_rate(query_components[component_index].strip())
        if rate is not None:
            component_index += 1

    topk = None
    if component_index < len(query_components):
        topk = parse_topk(query_components[component_index].strip())
        if topk is not None:
            component_index += 1

    if component_index >= len(query_components):
        raise OpenTSDBParseError(f"Illegal query string: `{query_string}`.")

    metric_string = ":".join(query_components[component_index:]).strip()
    tenant, metric, metric_suffix = _parse_truncate_tenant_metricname(metric_string)
    metric_suffix, multifields = _parse_truncate_multifields(metric_suffix)
    groups: list[TagKv] = []
    filters: list[TagKv] = []

    if metric_suffix:
        groups, metric_suffix = _parse_truncate_grouptagkvs(metric_suffix)

    if metric_suffix:
        if not metric_suffix.startswith("{") or not metric_suffix.endswith("}"):
            raise OpenTSDBParseError(f"Illegal metric tagkv string: `{metric_suffix}`.")
        filters = [
            parse_tagkv(tagkv_string.strip(), False)
            for tagkv_string in metric_suffix[1:-1].split(",")
            if tagkv_string.strip()
        ]

    return _build_model(
        lambda: Query(
            aggregator=aggregator,
            downsampling=downsampling,
            rate=rate,
            topk=topk,
            tenant=tenant,
            metric=metric,
            groups=groups,
            filters=filters,
            multifields=multifields,
        ),
        query_string,
    )


def _parse_truncate_grouptagkvs(metric_string: str) -> tuple[list[TagKv], str]:
    """解析 metric 后缀中的 group Tag 条件并返回剩余字符串。

    输入必须以 `{` 开头。函数会解析第一段花括号中的 group Tag 条件，
    并返回 `(groups, rest)`，其中 `rest` 是尚未解析的 filter Tag 后缀。
    这种“解析当前段并截断”的设计用于让完整 query parser 按顺序消费 metric 后缀。
    """
    if not metric_string.startswith("{"):
        raise OpenTSDBParseError(f"Illegal metric tagkv string: `{metric_string}`.")

    group_tagkvs_end_index = metric_string.find("}{")
    if group_tagkvs_end_index == -1:
        if not metric_string.endswith("}"):
            raise OpenTSDBParseError(f"Illegal metric tagkv string: `{metric_string}`.")
        group_tagkvs_string = metric_string[1:-1]
    else:
        group_tagkvs_string = metric_string[1:group_tagkvs_end_index]

    groups = [
        parse_tagkv(tagkv_string.strip(), True)
        for tagkv_string in group_tagkvs_string.split(",")
        if tagkv_string.strip()
    ]
    return groups, metric_string[len(group_tagkvs_string) + 2 :]


def _parse_truncate_tenant_metricname(metric_string: str) -> tuple[str, str, str]:
    """解析 tenant 与 metric 名称并返回 metric 后缀。

    - 支持 `[tenant]metric` 和 `metric` 两种形式。
    - 未提供 tenant 时返回 `default`。
    - 函数返回 `(tenant, metric, suffix)`，其中 `suffix` 是从 group/filter 花括号或 multifield 方括号开始的未解析后缀。
    """
    if metric_string.startswith("["):
        tenant_end_index = metric_string.find("]")
        if tenant_end_index == -1:
            raise OpenTSDBParseError(f"Illegal metric string: `{metric_string}`.")
        tenant = metric_string[1:tenant_end_index].strip()
        metric_string = metric_string[tenant_end_index + 1 :]
    else:
        tenant = "default"

    tagkv_start_index = metric_string.find("{")
    multifield_start_index = metric_string.find("[")
    suffix_start_indexes = [index for index in (tagkv_start_index, multifield_start_index) if index != -1]
    suffix_start_index = min(suffix_start_indexes) if suffix_start_indexes else -1

    if suffix_start_index == -1:
        return tenant, metric_string.strip(), ""
    return tenant, metric_string[:suffix_start_index].strip(), metric_string[suffix_start_index:]


def _parse_truncate_multifields(metric_string: str) -> tuple[str, MultiField | None]:
    """解析 metric 后缀末尾的多值字段配置并返回剩余字符串。

    - 只有当输入以 `]` 结尾时才尝试解析 multifield。
    - 函数返回 `(rest, multifields)`，其中 `rest` 是移除末尾 multifield 后剩余的 group/filter 后缀。
    - 没有 multifield 时原样返回输入和 `None`。
    """
    if not metric_string.endswith("]"):
        return metric_string, None

    multifields_start_index = metric_string.rfind("[")
    if multifields_start_index == -1:
        raise OpenTSDBParseError(f"Illegal metric string: `{metric_string}`.")

    multifields = parse_multifield(metric_string[multifields_start_index + 1 : -1])
    return metric_string[:multifields_start_index], multifields
