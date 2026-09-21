from pathlib import Path
import sys

import pandas as pd
import pytest

sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.comps import (
    calculate_ev_to_ebitda,
    calculate_price_to_earnings,
    calculate_implied_enterprise_value,
    calculate_implied_equity_value,
    build_company_comps_data,
    build_comps_table,
    calculate_median_multiples,
    get_target_comps_data,
    calculate_comps_valuation,
    build_comps_valuation,
)


def test_calculate_ev_to_ebitda():
    result = calculate_ev_to_ebitda(
        comp_enterprise_value=1000,
        comp_ebitda=100,
    )

    assert result == pytest.approx(10)


def test_calculate_price_to_earnings():
    result = calculate_price_to_earnings(
        comp_equity_value=1200,
        comp_net_income=100,
    )

    assert result == pytest.approx(12)


def test_calculate_implied_enterprise_value():
    result = calculate_implied_enterprise_value(
        target_ebitda=200,
        ev_to_ebitda=10,
    )

    assert result == pytest.approx(2000)


def test_calculate_implied_equity_value():
    result = calculate_implied_equity_value(
        target_net_income=150,
        price_to_earnings=12,
    )

    assert result == pytest.approx(1800)


def test_build_company_comps_data():
    historical_data = pd.DataFrame(
        {
            "diluted_shares": [100],
            "cash": [200],
            "total_debt": [500],
            "ebitda": [300],
            "net_income": [100],
        }
    )

    market_data = {
        "share_price": 50,
    }

    result = build_company_comps_data(
        historical_data,
        market_data,
    )

    assert result["market_cap"] == pytest.approx(5000)
    assert result["enterprise_value"] == pytest.approx(5300)
    assert result["ev_to_ebitda"] == pytest.approx(17.6666667)
    assert result["price_to_earnings"] == pytest.approx(50)


def test_build_comps_table(monkeypatch):
    historical_data = pd.DataFrame(
        {
            "diluted_shares": [100],
            "cash": [200],
            "total_debt": [500],
            "ebitda": [300],
            "net_income": [100],
        }
    )

    market_data = {
        "share_price": 50,
    }

    def mock_get_company_data(ticker):
        return {"ticker": ticker}

    def mock_normalise_historical_data(data):
        return historical_data

    def mock_get_market_data(data):
        return market_data

    monkeypatch.setattr(
        "src.comps.get_company_data",
        mock_get_company_data,
    )

    monkeypatch.setattr(
        "src.comps.normalise_historical_data",
        mock_normalise_historical_data,
    )

    monkeypatch.setattr(
        "src.comps.get_market_data",
        mock_get_market_data,
    )

    result = build_comps_table(["KO", "PEP"])

    assert list(result["ticker"]) == ["KO", "PEP"]
    assert len(result) == 2

    assert result["market_cap"].tolist() == [5000, 5000]
    assert result["enterprise_value"].tolist() == [5300, 5300]
    assert result["ev_to_ebitda"].tolist() == pytest.approx(
        [17.6666667, 17.6666667]
    )
    assert result["price_to_earnings"].tolist() == pytest.approx(
        [50, 50]
    )


def test_calculate_median_multiples():
    comps = pd.DataFrame(
        {
            "ev_to_ebitda": [10, 12, 15, 20, 25],
            "price_to_earnings": [15, 18, 20, 25, 30],
        }
    )

    result = calculate_median_multiples(comps)

    assert result["ev_to_ebitda"] == pytest.approx(15)
    assert result["price_to_earnings"] == pytest.approx(20)


def test_get_target_comps_data():
    historical_data = pd.DataFrame(
        {
            "ebitda": [300],
            "net_income": [100],
            "total_debt": [500],
            "cash": [200],
            "diluted_shares": [100],
        }
    )

    result = get_target_comps_data(historical_data)

    assert result == {
        "ebitda": 300,
        "net_income": 100,
        "debt": 500,
        "cash": 200,
        "diluted_shares": 100,
    }


def test_calculate_comps_valuation():
    median_multiples = {
        "ev_to_ebitda": 15,
        "price_to_earnings": 20,
    }

    result = calculate_comps_valuation(
        target_ebitda=200,
        target_net_income=100,
        target_debt=500,
        target_cash=200,
        target_diluted_shares=100,
        median_multiples=median_multiples,
    )

    assert result["implied_enterprise_value"] == pytest.approx(3000)
    assert result["implied_equity_value_ev"] == pytest.approx(2700)
    assert result["implied_share_price_ev"] == pytest.approx(27)
    assert result["implied_equity_value_pe"] == pytest.approx(2000)
    assert result["implied_share_price_pe"] == pytest.approx(20)


def test_build_comps_valuation(monkeypatch):
    target_historical_data = pd.DataFrame(
        {
            "ebitda": [200],
            "net_income": [100],
            "total_debt": [500],
            "cash": [200],
            "diluted_shares": [100],
        }
    )

    comps = pd.DataFrame(
        {
            "ticker": ["PEP", "MNST"],
            "ev_to_ebitda": [10, 20],
            "price_to_earnings": [15, 25],
        }
    )

    monkeypatch.setattr(
        "src.comps.build_comps_table_with_failures",
        lambda tickers: (comps, []),
    )

    result = build_comps_valuation(
        target_historical_data=target_historical_data,
        comparable_tickers=["PEP", "MNST"],
    )

    assert result["median_multiples"]["ev_to_ebitda"] == pytest.approx(15)
    assert result["median_multiples"]["price_to_earnings"] == pytest.approx(20)

    assert result["valuation"]["implied_enterprise_value"] == pytest.approx(3000)
    assert result["valuation"]["implied_equity_value_ev"] == pytest.approx(2700)
    assert result["valuation"]["implied_share_price_ev"] == pytest.approx(27)

    assert result["valuation"]["implied_equity_value_pe"] == pytest.approx(2000)
    assert result["valuation"]["implied_share_price_pe"] == pytest.approx(20)