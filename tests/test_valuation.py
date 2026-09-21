from pathlib import Path
import sys

import pandas as pd
import pytest

sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.valuation import build_valuation


def test_build_valuation():
    historical_data = pd.DataFrame(
        {
            "diluted_shares": [1000],
            "total_debt": [1000],
            "cash": [100],
        }
    )

    forecast = pd.DataFrame(
        {
            "fcff": [100, 110, 120],
        }
    )

    assumptions = {
        "wacc": {
            "share_price": 100,
            "risk_free_rate": 0.04,
            "beta": 1.2,
            "market_risk_premium": 0.05,
            "cost_of_debt": 0.05,
            "tax_rate": 0.20,
        },
        "terminal": {
            "growth_rate": 0.03,
        },
    }

    market_data = {
    "share_price": 100,
    }

    result = build_valuation(
        historical_data,
        forecast,
        market_data,
        assumptions,
    )

    assert result["wacc"] == pytest.approx(0.09940594)

    assert result["enterprise_value"] > 0

    assert result["equity_value"] == pytest.approx(
        result["enterprise_value"]
        - historical_data["total_debt"].iloc[-1]
        + historical_data["cash"].iloc[-1]
    )

    assert result["implied_share_price"] == pytest.approx(
        result["equity_value"]
        / historical_data["diluted_shares"].iloc[-1]
    )