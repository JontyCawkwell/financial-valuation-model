from pathlib import Path
import sys
import pytest

sys.path.append(str(Path(__file__).resolve().parent.parent))
from src.data import load_historical_data
from src.assumptions import load_assumptions
from src.forecasts import (
    calculate_change_in_nwc,
    calculate_nopat,
    forecast_capex,
    forecast_da,
    forecast_ebit,
    forecast_nwc,
    forecast_revenue,
    forecast_tax,
    build_forecast
)


def test_forecast_revenue():
    assert forecast_revenue(100, 0.10) == pytest.approx(110)


def test_forecast_ebit():
    assert forecast_ebit(110, 0.20) == pytest.approx(22)


def test_forecast_tax():
    assert forecast_tax(22, 0.25) == pytest.approx(5.5)


def test_calculate_nopat():
    assert calculate_nopat(22, 5.5) == pytest.approx(16.5)


def test_forecast_da():
    assert forecast_da(110, 0.05) == pytest.approx(5.5)


def test_forecast_capex():
    assert forecast_capex(110, 0.06) == pytest.approx(6.6)


def test_forecast_nwc():
    assert forecast_nwc(110, 0.10) == pytest.approx(11)


def test_calculate_change_in_nwc():
    assert calculate_change_in_nwc(120, 100) == pytest.approx(20)


def test_build_forecast():
    historical_data = load_historical_data()
    assumptions = load_assumptions()

    forecast = build_forecast(
        historical_data,
        assumptions,
    )

    forecast_assumptions = assumptions["forecast"]

    assert len(forecast) == 5
    assert list(forecast["year"]) == [2026, 2027, 2028, 2029, 2030]

    # Check all forecast outputs were calculated.
    for column in [
        "revenue",
        "ebit",
        "tax",
        "nopat",
        "da",
        "capex",
        "nwc",
        "change_in_nwc",
        "fcff",
    ]:
        assert forecast[column].notna().all()

    # Check 2026 revenue uses 2025 revenue and the 2026 growth assumption.
    expected_2026_revenue = (
        historical_data.iloc[-1]["revenue"]
        * (1 + forecast_assumptions["revenue_growth"][2026])
    )

    assert forecast.loc[0, "revenue"] == pytest.approx(
        expected_2026_revenue
    )

    # Check 2027 revenue uses the forecast 2026 revenue.
    expected_2027_revenue = (
        expected_2026_revenue
        * (1 + forecast_assumptions["revenue_growth"][2027])
    )

    assert forecast.loc[1, "revenue"] == pytest.approx(
        expected_2027_revenue
    )

    # Check EBIT uses the forecast EBIT margin.
    assert forecast.loc[0, "ebit"] == pytest.approx(
        forecast.loc[0, "revenue"]
        * forecast_assumptions["ebit_margin"][2026]
    )

    # Check tax uses the forecast tax rate.
    assert forecast.loc[0, "tax"] == pytest.approx(
        forecast.loc[0, "ebit"]
        * forecast_assumptions["tax_rate"]
    )

    # Check NOPAT.
    assert forecast.loc[0, "nopat"] == pytest.approx(
        forecast.loc[0, "ebit"] - forecast.loc[0, "tax"]
    )

    # Check FCFF follows the DCF formula.
    expected_2026_fcff = (
        forecast.loc[0, "nopat"]
        + forecast.loc[0, "da"]
        - forecast.loc[0, "capex"]
        - forecast.loc[0, "change_in_nwc"]
    )

    assert forecast.loc[0, "fcff"] == pytest.approx(
        expected_2026_fcff
    )

    # Check 2026 change in NWC uses 2025 historical NWC as the starting point.
    historical_nwc = (
        historical_data.iloc[-1]["accounts_receivable"]
        + historical_data.iloc[-1]["inventories"]
        - historical_data.iloc[-1]["accounts_payable"]
    )

    assert forecast.loc[0, "change_in_nwc"] == pytest.approx(
        forecast.loc[0, "nwc"] - historical_nwc
    )

    # Check 2027 change in NWC uses 2026 forecast NWC.
    assert forecast.loc[1, "change_in_nwc"] == pytest.approx(
        forecast.loc[1, "nwc"] - forecast.loc[0, "nwc"]
    )