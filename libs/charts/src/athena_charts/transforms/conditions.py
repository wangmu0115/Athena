from athena_charts.specs.rules import DataCondition, DataPredicate
from athena_charts.transforms.data_context import DataPointContext


def evaluate_data_predicate(
    predicate: DataPredicate,
    *,
    context: DataPointContext,
) -> bool:
    """判断单个数据谓词是否满足。"""
    resolved_data = context.get(predicate.field)
    if resolved_data is None:
        return False

    checks: list[bool] = []
    if predicate.gt is not None:
        checks.append(resolved_data > predicate.gt)

    if predicate.gte is not None:
        checks.append(resolved_data >= predicate.gte)

    if predicate.lt is not None:
        checks.append(resolved_data < predicate.lt)

    if predicate.lte is not None:
        checks.append(resolved_data <= predicate.lte)

    if predicate.eq is not None:
        checks.append(resolved_data == predicate.eq)

    if predicate.neq is not None:
        checks.append(resolved_data != predicate.neq)

    return False if not checks else all(checks)


def evaluate_data_condition(
    condition: DataCondition,
    *,
    context: DataPointContext,
) -> bool:
    """判断数据条件表达式是否满足。

    `all` 中的谓词必须全部满足，`any` 中的谓词满足任意一个即可。如果同时配置了 `all` 和 `any`，则二者都需要满足。
    """
    if not condition.all and not condition.any:
        return False

    if condition.any and not any(
        evaluate_data_predicate(
            predicate,
            context=context,
        )
        for predicate in condition.any
    ):
        return False

    if condition.all and not all(  # noqa: SIM103
        evaluate_data_predicate(
            predicate,
            context=context,
        )
        for predicate in condition.all
    ):
        return False

    return True
