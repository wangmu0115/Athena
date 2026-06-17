import importlib
from datetime import date

import pytest
from pydantic import BaseModel

pd = pytest.importorskip("pandas")
tabular = importlib.import_module("athena_kit.core.tabular")

SourceCell = tabular.SourceCell
dataframe_to_models = tabular.dataframe_to_models


class SourceModel(BaseModel):
    trade_date: date = SourceCell(required=True)
    symbol: str = SourceCell(source="代码")
    amount: int = SourceCell(source="成交额")


def test_dataframe_to_models_with_extra_fields_and_sources():
    df = pd.DataFrame([{"代码": "000001", "成交额": 100}])

    assert dataframe_to_models(
        df,
        SourceModel,
        extra_fields={"trade_date": date(2026, 5, 19)},
        strict=False,
    ) == [SourceModel(trade_date=date(2026, 5, 19), symbol="000001", amount=100)]
