from pathlib import Path
import sys
import pytest


sys.path.append(str(Path(__file__).resolve().parent.parent))
from src.comps import (
    calculate_ev_to_ebitda,
    calculate_implied_enterprise_value,
    calculate_implied_equity_value,
    calculate_price_to_earnings,
)


def test_calculate_ev_to_ebitda():
    result = calculate_ev_to_ebitda(
        enterprise_value=1000,
        ebitda=100,
    )

    assert result == pytest.approx(10)


def test_calculate_price_to_earnings():
    result = calculate_price_to_earnings(
        equity_value=1000,
        net_income=100,
    )

    assert result == pytest.approx(10)


def test_calculate_implied_enterprise_value():
    result = calculate_implied_enterprise_value(
        ebitda=100,
        ev_to_ebitda=10,
    )

    assert result == pytest.approx(1000)


def test_calculate_implied_equity_value():
    result = calculate_implied_equity_value(
        net_income=100,
        price_to_earnings=10,
    )

    assert result == pytest.approx(1000)