from athena_charts.resolved import ResolvedDataLabelStyle
from athena_charts.resolved.styles import ResolvedMarkerStyle
from athena_charts.specs.plots.options import DataLabelOptions
from athena_charts.specs.plots.options.markers import MarkerOptions
from athena_charts.transforms.conditions import evaluate_data_condition
from athena_charts.transforms.data_context import DataPointContext


def resolve_data_label_style(
    options: DataLabelOptions,
    *,
    context: DataPointContext,
) -> ResolvedDataLabelStyle:
    """解析数据标签最终生效的运行时样式。

    该函数会基于：
        - `DataLabelOptions` 中的默认样式
        - `dynamic_rules` 中的动态样式规则
        - 当前数据点的上下文数据
    计算得到最终用于渲染的数据标签样式，样式解析流程：
        1. 先使用 `DataLabelOptions` 中的默认样式初始化结果。
        2. 按顺序遍历 `dynamic_rules`。
        3. 当规则条件满足时，将规则中的非空字段覆盖到当前结果中。
        4. 后匹配的规则可以覆盖前面规则产生的样式。

    Args:
        options: 数据标签配置。
        context: 单个数据点的运行时上下文。

    Returns:
        最终解析后的数据标签运行时样式。
    """
    resolved = ResolvedDataLabelStyle(
        color=options.color,
        fontsize=options.fontsize,
        fontweight=options.fontweight,
    )

    for rule in options.style_rules:
        if evaluate_data_condition(rule.when, context=context):
            if rule.color is not None:
                resolved.color = rule.color
            if rule.fontsize is not None:
                resolved.fontsize = rule.fontsize
            if rule.fontweight is not None:
                resolved.fontweight = rule.fontweight

    return resolved


def resolve_marker_style(
    options: MarkerOptions,
    *,
    context: DataPointContext,
) -> ResolvedMarkerStyle:
    """解析数据点标记最终生效的运行时样式。

    该函数会基于：
        - `MarkerOptions` 中的默认样式
        - `style_rules` 中的动态样式规则
        - 当前数据点的上下文数据
    计算得到最终用于渲染的数据点标记样式，样式解析流程：
        1. 先使用 `MarkerOptions` 中的默认样式初始化结果。
        2. 按顺序遍历 `style_rules`。
        3. 当规则条件满足时，将规则中的非空字段覆盖到当前结果中。
        4. 后匹配的规则可以覆盖前面规则产生的样式。

    Args:
        options: 数据点标记配置。
        context: 单个数据点的运行时上下文。

    Returns:
        最终解析后的数据点标记运行时样式。
    """
    resolved = ResolvedMarkerStyle(
        shape=options.shape,
        size=options.size,
        color=options.color,
        edge_color=options.edge_color,
        edge_width=options.edge_width,
        alpha=options.alpha,
        z_index=options.z_index,
    )

    for rule in options.style_rules:
        if evaluate_data_condition(rule.when, context=context):
            if rule.shape is not None:
                resolved.shape = rule.shape
            if rule.size is not None:
                resolved.size = rule.size
            if rule.color is not None:
                resolved.color = rule.color
            if rule.edge_color is not None:
                resolved.edge_color = rule.edge_color
            if rule.edge_width is not None:
                resolved.edge_width = rule.edge_width
            if rule.alpha is not None:
                resolved.alpha = rule.alpha
            if rule.z_index is not None:
                resolved.z_index = rule.z_index

    return resolved
