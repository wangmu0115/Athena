import importlib
from datetime import date

import pytest
from pydantic import BaseModel

pd = pytest.importorskip("pandas")
tabular = importlib.import_module("athena_kit.core.tabular")

SourceCell = tabular.SourceCell
TableCell = tabular.TableCell
TableRow = tabular.TableRow
dataframe_to_models = tabular.dataframe_to_models
table_rows_to_dataframe = tabular.table_rows_to_dataframe


class SourceModel(BaseModel):
    trade_date: date = SourceCell(required=True)
    symbol: str = SourceCell(source="代码")
    amount: int = SourceCell(source="成交额")


class RowModel(TableRow):
    symbol: str = TableCell(title="股票代码", order=1)
    amount: int = TableCell(title="成交额", order=2)


def test_dataframe_to_models_with_extra_fields_and_sources():
    df = pd.DataFrame([{"代码": "000001", "成交额": 100}])

    assert dataframe_to_models(
        df,
        SourceModel,
        extra_fields={"trade_date": date(2026, 5, 19)},
        strict=False,
    ) == [SourceModel(trade_date=date(2026, 5, 19), symbol="000001", amount=100)]


def test_table_rows_to_dataframe_uses_table_headers():
    df = table_rows_to_dataframe([RowModel(symbol="000001", amount=100)])

    assert list(df.columns) == ["股票代码", "成交额"]
    assert df.to_dict("records") == [{"股票代码": "000001", "成交额": 100}]
