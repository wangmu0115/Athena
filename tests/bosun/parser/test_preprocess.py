import pytest

from athena_kit.bosun.parser.exceptions import BosunPreprocessError
from athena_kit.bosun.parser.preprocess import preprocess


def test_preprocess_expands_query_expression_variables():
    source = """
    $err = q("sum:service.error", "5m", "")
    $total = q("sum:service.total", "5m", "")

    1 - (avg($err) / (avg($total) + 1e-16))
    """

    assert (
        preprocess(source)
        == '1 - (avg(q("sum:service.error", "5m", "")) / (avg(q("sum:service.total", "5m", "")) + 1e-16))'
    )


def test_preprocess_alert_definition_uses_warn_expression_and_ignores_metadata():
    source = """
    nullAsZero = false
    $expr_0 = avg(q("sum:service.error", "5m", "")) > 100
    $expr_1 = avg(q("sum:service.total", "5m", "")) < 10
    warn = $expr_0 || $expr_1
    runEvery = 1
    """

    assert (
        preprocess(source)
        == 'avg(q("sum:service.error", "5m", "")) > 100 || avg(q("sum:service.total", "5m", "")) < 10'
    )


def test_preprocess_supports_split_by_colon_placeholder():
    source = """
    $service = checkout:payment
    $metric = service.${service:splitByColon:1}.qps

    q("sum:$metric", "5m", "")
    """

    assert preprocess(source) == 'q("sum:service.payment.qps", "5m", "")'


def test_preprocess_rejects_variable_assignment_after_expression():
    source = """
    q("sum:service.qps", "5m", "")
    $late = q("sum:late", "5m", "")
    """

    with pytest.raises(BosunPreprocessError, match="Variable assignment cannot appear after expression entry"):
        preprocess(source)


def test_preprocess_rejects_missing_expression_entry():
    with pytest.raises(BosunPreprocessError, match="does not contain an expression entry"):
        preprocess("$metric = service.qps")
