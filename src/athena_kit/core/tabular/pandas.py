from typing import Any

from pydantic import BaseModel

try:
    import pandas as pd
except ImportError as exc:
    # pragma: no cover - exercised only without optional dependency.
    msg = "athena_kit.core.tabular.pandas requires `pandas`. Install it with `athena-kit[pandas]`."
    raise ImportError(msg) from exc


def dataframe_to_models[T: BaseModel](
    df: pd.DataFrame,
    model_cls: type[T],
    *,
    extra_fields: dict[str, Any] | None = None,
    strict: bool = True,
) -> list[T]:
    """将 pandas DataFrame 转换为 Pydantic 模型列表。

    该函数适合读取外部二维数据，并将每一行映射为一个 Pydantic 模型实例。
    目标模型字段可以使用 `SourceCell` 声明来源列、必填策略和转换函数，未使用 `SourceCell` 的字段会默认尝试读取同名列。

    字段解析规则：
        - 如果字段通过 `SourceCell(source=...)` 声明来源列，会优先从这些列名中读取值。
        - 如果未声明 `source`，会使用模型字段名作为来源列名。
        - 如果 DataFrame 中没有匹配列，但 `extra_fields` 中存在同名字段，则使用 `extra_fields` 的值。
        - 如果字段声明了 `SourceCell(transform=...)`，会在读取并归一化空值后调用该转换函数。
        - `None`、空白字符串和 pandas 空值会被视为 `None`。

    Args:
        df: 来源 DataFrame。
        model_cls: 目标 Pydantic 模型类，字段可使用 `SourceCell` 补充来源映射元信息。
        extra_fields: 可选的额外字段值，用于补充 DataFrame 中不存在的字段。
        strict: 是否在映射阶段对缺失来源列提前抛出 `ValueError`。

    Returns:
        转换并通过 `model_cls.model_validate()` 校验后的模型列表。
    """
    extra_fields = extra_fields or {}
    rows = []

    for row_index, record in df.iterrows():
        payload = {}
        for field_name, field in model_cls.model_fields.items():
            value = _parse_field_value(
                record=record,
                field_name=field_name,
                field_extra=_normalize_field_extra(field.json_schema_extra),
                extra_fields=extra_fields,
                strict=strict,
                row_index=row_index,
            )
            payload[field_name] = value

        rows.append(model_cls.model_validate(payload))

    return rows


def _parse_field_value(
    *,
    record: pd.Series,
    field_name: str,
    field_extra: dict[str, Any],
    extra_fields: dict[str, Any],
    strict: bool,
    row_index: Any,
) -> Any:
    source = field_extra.get("source")
    required = bool(field_extra.get("required", False))
    transform = field_extra.get("transform")

    # 解析所有的 source 字段
    source_candidates = _normalize_sources(source, field_name)

    found = False  # 是否成功映射到值
    value = None  # 映射值
    used_source = None  # 使用的来源字段
    for source_candidate in source_candidates:
        if source_candidate in record:
            found = True
            value = record.get(source_candidate)
            used_source = source_candidate
            break

    if not found and field_name in extra_fields:
        found = True
        value = extra_fields.get(field_name)
        used_source = f"extra_fields.{field_name}"

    if not found and (strict or required):
        raise ValueError(
            f"Missing source column for field {field_name} at row {row_index}, candidates={source_candidates}.",
        )

    value = _normalize_pandas_value(value)
    if value is None:
        return None

    if transform is not None:
        try:
            value = transform(value)
        except Exception as exc:
            raise ValueError(
                f"Transform failed for field {field_name} at row {row_index}, source={used_source}, value={value!r}.",
            ) from exc

    return value


def _normalize_field_extra(field_extra: Any) -> dict[str, Any]:
    if isinstance(field_extra, dict):
        return field_extra

    return {}


def _normalize_sources(source: str | list[str] | tuple[str, ...] | None, field_name: str) -> list[str]:
    if source is None:
        return [field_name]

    if isinstance(source, str):
        return [source, field_name]

    return [*source, field_name]


def _normalize_pandas_value(value: Any) -> Any:
    if value is None:
        return None

    try:
        if pd.isna(value):
            return None
    except (TypeError, ValueError):
        pass

    return value
