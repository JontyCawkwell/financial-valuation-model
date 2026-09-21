import pandas as pd
from pathlib import Path
import sys

import pytest

sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.assumptions import (
    load_assumptions,
    calculate_historical_average,
    calculate_historical_growth,
    calculate_historical_margin,
    calculate_historical_tax_rate,
    build_historical_assumptions,
    build_forecast_assumptions,
)


def test_load_assumptions():
    assumptions = load_assumptions()

    assert isinstance(assumptions, dict)
    assert "terminal" in assumptions
    assert "wacc" in assumptions


def test_calculate_historical_average():
    data = pd.DataFrame({"value": [10, 20, 30]})

    assert calculate_historical_average(data, "value") == 20


def test_calculate_historical_growth():
    data = pd.DataFrame({"value": [100, 110, 121]})

    assert round(calculate_historical_growth(data, "value"), 6) == 0.10


def test_calculate_historical_margin():
    data = pd.DataFrame({
        "profit": [10, 20, 30],
        "revenue": [100, 200, 300],
    })

    assert calculate_historical_margin(
        data, "profit", "revenue"
    ) == pytest.approx(0.1)


def test_calculate_historical_tax_rate():
    data = pd.DataFrame({
        "pretax_income": [90, 180, 270],
        "income_tax_expense": [18, 36, 54],
    })

    assert calculate_historical_tax_rate(data) == pytest.approx(0.2)


def test_build_forecast_assumptions():
    historical_data = pd.DataFrame(
        {
            "revenue": [100, 110, 121],
            "operating_income": [20, 22, 24.2],
            "pretax_income": [15, 17, 19.2],
            "income_tax_expense": [3, 3.4, 3.84],
            "depreciation_amortisation": [5, 5.5, 6],
            "capex": [4, 4.4, 4.8],
        }
    )

    assumptions = {
        "terminal": {
            "growth_rate": 0.025,
        }
    }

    result = build_forecast_assumptions(
        historical_data,
        assumptions,
    )

    historical_assumptions = build_historical_assumptions(
        historical_data
    )

    assert result["forecast"]["revenue_growth"][2026] == pytest.approx(
        historical_assumptions["revenue_growth"]
    )

    assert result["forecast"]["revenue_growth"][2030] == pytest.approx(
        0.025
    )

    assert result["forecast"]["ebit_margin"][2026] == pytest.approx(
        historical_assumptions["ebit_margin"]
    )

    assert result["forecast"]["tax_rate"] == pytest.approx(
        historical_assumptions["tax_rate"]
    )