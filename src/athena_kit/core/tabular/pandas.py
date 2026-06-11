from typing import TYPE_CHECKING, Any

from pydantic import BaseModel

from athena_kit.core.tabular.row import TableRow

try:
    import pandas as pd
except ImportError as exc:  # pragma: no cover - exercised only without optional dependency.
    msg = "athena_kit.core.tabular.pandas requires pandas. Install it with `athena-kit[dataframe]`."
    raise ImportError(msg) from exc

if TYPE_CHECKING:
    from pandas import DataFrame, Series
else:
    DataFrame = pd.DataFrame
    Series = pd.Series


def dataframe_to_models[T: BaseModel](
    df: DataFrame,
    model_cls: type[T],
    *,
    extra_fields: dict[str, Any] | None = None,
    strict: bool = True,
) -> list[T]:
    """将 pandas DataFrame 转换为 Pydantic 模型列表。"""
    extra_fields = extra_fields or {}
    rows = []

    for row_index, record in df.iterrows():
        payload = {}
        for field_name, field in model_cls.model_fields.items():
            value = _parse_field_value(
                record=record,
                field_name=field_name,
                field_extra=field.json_schema_extra or {},
                extra_fields=extra_fields,
                strict=strict,
                row_index=row_index,
            )
            payload[field_name] = value
        rows.append(model_cls.model_validate(payload))

    return rows


def models_to_dataframe(models: list[BaseModel], *, by_alias: bool = True) -> DataFrame:
    """将 Pydantic 模型列表转换为 pandas DataFrame。"""
    if not models:
        return pd.DataFrame()

    return pd.DataFrame([model.model_dump(by_alias=by_alias) for model in models])


def table_rows_to_dataframe(rows: list[BaseModel]) -> DataFrame:
    """将表格行模型列表转换为 pandas DataFrame。"""
    if not rows:
        return pd.DataFrame()

    row_type = rows[0].__class__
    if issubclass(row_type, TableRow):
        return pd.DataFrame(
            [row.to_table_row() for row in rows],
            columns=row_type.table_headers(),
        )

    return models_to_dataframe(rows, by_alias=True)


def _parse_field_value(
    *,
    record: Series,
    field_name: str,
    field_extra: dict[str, Any],
    extra_fields: dict[str, Any],
    strict: bool,
    row_index: Any,
) -> Any:
    source = field_extra.get("source")
    required = bool(field_extra.get("required", False))
    transform = field_extra.get("transform")

    source_candidates = _normalize_sources(source, field_name)

    found = False
    value = None
    used_source = None
    for candidate in source_candidates:
        if candidate in record:
            found = True
            value = record.get(candidate)
            used_source = candidate
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
