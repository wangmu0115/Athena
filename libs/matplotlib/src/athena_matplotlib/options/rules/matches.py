from athena_matplotlib.options.rules.conditions import DataCondition, DataPredicate
from athena_matplotlib.options.rules.data_content import CartesianDataContent


def match_data_predicate(
    predicate: DataPredicate,
    *,
    context: CartesianDataContent,
) -> bool:
    """判断单个数据谓词是否满足。

    - 如果字段值为 `None`，则返回值为 `False`。
    - 不设置任何条件时，返回值为 `True`。
    - 不为空的条件都满足时，返回值才为 `True`。
    """
    value = context.get(predicate.field)
    if value is None:
        return False

    if predicate.gt_ is not None and not value > predicate.gt_:
        return False
    if predicate.gte_ is not None and not value >= predicate.gte_:
        return False
    if predicate.lt_ is not None and not value < predicate.lt_:
        return False
    if predicate.lte_ is not None and not value <= predicate.lte_:
        return False
    if predicate.eq_ is not None and value != predicate.eq_:
        return False
    if predicate.neq_ is not None and value == predicate.neq_:  # noqa: SIM103
        return False

    return True


def match_data_condition(
    condition: DataCondition,
    *,
    context: CartesianDataContent,
) -> bool:
    """判断数据条件表达式是否满足。

    - `all_` 中的谓词必须全部满足，`any_` 中的谓词满足任意一个即可。
    - 如果没有配置任何谓语条件，则返回值为 `False`。
    """

    if condition.all_:
        return all(match_data_predicate(predicate, context=context) for predicate in condition.all_)

    if condition.any_:
        return any(match_data_predicate(predicate, context=context) for predicate in condition.all_)

    return False
