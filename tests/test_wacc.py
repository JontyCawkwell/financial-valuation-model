from pathlib import Path
import sys

import pytest

sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.wacc import (
    calculate_after_tax_cost_of_debt,
    calculate_cost_of_equity,
    calculate_wacc,
)


def test_calculate_cost_of_equity():
    result = calculate_cost_of_equity(
        risk_free_rate=0.04,
        beta=1.2,
        market_risk_premium=0.05,
    )

    assert result == pytest.approx(0.10)


def test_calculate_after_tax_cost_of_debt():
    result = calculate_after_tax_cost_of_debt(
        cost_of_debt=0.05,
        tax_rate=0.20,
    )

    assert result == pytest.approx(0.04)


def test_calculate_wacc():
    result = calculate_wacc(
        market_value_equity=800,
        debt=200,
        cost_of_equity=0.10,
        cost_of_debt=0.05,
        tax_rate=0.20,
    )

    assert result == pytest.approx(0.088)