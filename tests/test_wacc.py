from pathlib import Path
import sys

import pytest
import pandas as pd

sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.wacc import (
    calculate_after_tax_cost_of_debt,
    calculate_cost_of_equity,
    calculate_market_value_equity,
    calculate_total_debt,
    calculate_wacc,
    build_wacc,
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


def test_calculate_market_value_equity():
    result = calculate_market_value_equity(
        share_price=100,
        diluted_shares=1000,
    )

    assert result == pytest.approx(100000)


def test_calculate_total_debt():
    result = calculate_total_debt(
        short_term_debt=200,
        long_term_debt=800,
    )

    assert result == pytest.approx(1000)


def test_calculate_wacc():
    result = calculate_wacc(
        market_value_equity=800,
        debt=200,
        cost_of_equity=0.10,
        cost_of_debt=0.05,
        tax_rate=0.20,
    )

    assert result == pytest.approx(0.088)


def test_build_wacc():
    historical_data = pd.DataFrame(
        {
            "diluted_shares": [1000],
            "total_debt": [1000],
            "operating_income": [100],
            "pretax_income": [90],
            "income_tax_expense": [18],
        }
    )

    assumptions = {
        "wacc": {
            "market_risk_premium": 0.05,
            "cost_of_debt": 0.05,
        }
    }

    market_data = {
        "share_price": 100,
        "risk_free_rate": 0.04,
        "beta": 1.2,
    }

    result = build_wacc(
        historical_data,
        market_data,
        assumptions,
    )

    assert result == pytest.approx(0.09940594)