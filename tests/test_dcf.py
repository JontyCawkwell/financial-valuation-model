from pathlib import Path
import sys

import pytest
import pandas as pd

sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.dcf import (
    calculate_fcff,
    calculate_terminal_value_exit_multiple,
    calculate_terminal_value_perpetuity,
    discount_cash_flow,
    build_dcf,
    calculate_equity_value,
    calculate_implied_share_price,
)


def test_calculate_fcff():
    result = calculate_fcff(
        nopat=800,
        depreciation_amortisation=100,
        capex=150,
        change_in_nwc=50,
    )

    assert result == pytest.approx(700)


def test_discount_cash_flow():
    result = discount_cash_flow(
        cash_flow=100,
        discount_rate=0.10,
        period=2,
    )

    assert result == pytest.approx(82.6446)


def test_calculate_terminal_value_perpetuity():
    result = calculate_terminal_value_perpetuity(
        final_fcff=100,
        wacc=0.08,
        terminal_growth_rate=0.03,
    )

    assert result == pytest.approx(2060)


def test_calculate_terminal_value_exit_multiple():
    result = calculate_terminal_value_exit_multiple(
        final_ebitda=500,
        exit_multiple=10,
    )

    assert result == pytest.approx(5000)


def test_build_dcf():
    forecast = pd.DataFrame(
        {
            "fcff": [100, 110, 120],
        }
    )

    result = build_dcf(
        forecast=forecast,
        wacc=0.10,
        terminal_growth_rate=0.03,
    )

    assert len(result["discounted_fcff"]) == len(forecast)

    assert result["discounted_terminal_value"] == pytest.approx(
        result["terminal_value"] / 1.10**3
)

    assert result["enterprise_value"] == pytest.approx(
        sum(result["discounted_fcff"])
        + result["discounted_terminal_value"]
    )


def test_calculate_equity_value():
    result = calculate_equity_value(
        enterprise_value=1000,
        debt=200,
        cash=100,
    )

    assert result == pytest.approx(900)


def test_calculate_implied_share_price():
    result = calculate_implied_share_price(
        equity_value=900,
        diluted_shares=100,
    )

    assert result == pytest.approx(9)