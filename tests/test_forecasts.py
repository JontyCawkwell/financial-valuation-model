from pathlib import Path
import sys
import pytest

sys.path.append(str(Path(__file__).resolve().parent.parent))
from src.forecasts import (
    calculate_change_in_nwc,
    calculate_nopat,
    forecast_capex,
    forecast_da,
    forecast_ebit,
    forecast_nwc,
    forecast_revenue,
    forecast_tax,
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