from pathlib import Path
import sys

import pytest

sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.dcf import (
    calculate_fcff,
    calculate_terminal_value_exit_multiple,
    calculate_terminal_value_perpetuity,
    discount_cash_flow,
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