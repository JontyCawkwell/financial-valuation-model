import pandas as pd
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.data_sources import (
    get_company_data,
    get_market_data,
    normalise_historical_data,
)


def calculate_ev_to_ebitda(
    comp_enterprise_value: float,
    comp_ebitda: float,
) -> float:
    """Calculate a comparable company's EV/EBITDA multiple."""
    return comp_enterprise_value / comp_ebitda


def calculate_price_to_earnings(
    comp_equity_value: float,
    comp_net_income: float,
) -> float:
    """Calculate a comparable company's P/E multiple."""
    return comp_equity_value / comp_net_income


def calculate_implied_enterprise_value(
    target_ebitda: float,
    ev_to_ebitda: float,
) -> float:
    """Calculate target implied enterprise value from an EV/EBITDA multiple."""
    return target_ebitda * ev_to_ebitda


def calculate_implied_equity_value(
    target_net_income: float,
    price_to_earnings: float,
) -> float:
    """Calculate target implied equity value from a P/E multiple."""
    return target_net_income * price_to_earnings


def build_company_comps_data(
    historical_data,
    market_data,
) -> dict:
    """Build comparable-company metrics from standardised company data."""

    latest = historical_data.iloc[-1]

    share_price = market_data["share_price"]
    diluted_shares = latest["diluted_shares"]
    cash = latest["cash"]
    debt = latest["total_debt"]
    ebitda = latest["ebitda"]
    net_income = latest["net_income"]

    market_cap = share_price * diluted_shares
    enterprise_value = market_cap + debt - cash

    return {
        "share_price": share_price,
        "market_cap": market_cap,
        "enterprise_value": enterprise_value,
        "ebitda": ebitda,
        "net_income": net_income,
        "ev_to_ebitda": calculate_ev_to_ebitda(
            enterprise_value,
            ebitda,
        ),
        "price_to_earnings": calculate_price_to_earnings(
            market_cap,
            net_income,
        ),
    }


def build_comps_table(
    tickers: list[str],
) -> pd.DataFrame:
    """Build comparable-company metrics for a list of tickers."""

    companies = []

    for ticker in tickers:
        data = get_company_data(ticker)

        historical_data = normalise_historical_data(data)
        market_data = get_market_data(data)

        company_data = build_company_comps_data(
            historical_data,
            market_data,
        )

        company_data["ticker"] = ticker.upper()

        companies.append(company_data)

    return pd.DataFrame(companies)


def calculate_median_multiples(
    comps: pd.DataFrame,
) -> dict:
    """Calculate median valuation multiples from comparable companies."""

    return {
        "ev_to_ebitda": comps["ev_to_ebitda"].median(),
        "price_to_earnings": comps["price_to_earnings"].median(),
    }


def get_target_comps_data(
    historical_data: pd.DataFrame,
) -> dict:
    """Extract the target company's data required for a comps valuation."""

    latest = historical_data.iloc[-1]

    return {
        "ebitda": latest["ebitda"],
        "net_income": latest["net_income"],
        "debt": latest["total_debt"],
        "cash": latest["cash"],
        "diluted_shares": latest["diluted_shares"],
    }


def calculate_comps_valuation(
    target_ebitda: float,
    target_net_income: float,
    target_debt: float,
    target_cash: float,
    target_diluted_shares: float,
    median_multiples: dict,
) -> dict:
    """Calculate target valuation using median comparable-company multiples."""

    implied_enterprise_value = calculate_implied_enterprise_value(
        target_ebitda=target_ebitda,
        ev_to_ebitda=median_multiples["ev_to_ebitda"],
    )

    implied_equity_value_ev = (
        implied_enterprise_value
        - target_debt
        + target_cash
    )

    implied_share_price_ev = (
        implied_equity_value_ev
        / target_diluted_shares
    )

    implied_equity_value_pe = calculate_implied_equity_value(
        target_net_income=target_net_income,
        price_to_earnings=median_multiples["price_to_earnings"],
    )

    implied_share_price_pe = (
        implied_equity_value_pe
        / target_diluted_shares
    )

    return {
        "implied_enterprise_value": implied_enterprise_value,
        "implied_equity_value_ev": implied_equity_value_ev,
        "implied_share_price_ev": implied_share_price_ev,
        "implied_equity_value_pe": implied_equity_value_pe,
        "implied_share_price_pe": implied_share_price_pe,
    }


def build_comps_valuation(
    target_historical_data: pd.DataFrame,
    comparable_tickers: list[str],
) -> dict:
    """Build a comparable-company valuation for the target company."""

    target_data = get_target_comps_data(
        target_historical_data
    )

    comps = build_comps_table(
        comparable_tickers
    )

    median_multiples = calculate_median_multiples(
        comps
    )

    valuation = calculate_comps_valuation(
        target_ebitda=target_data["ebitda"],
        target_net_income=target_data["net_income"],
        target_debt=target_data["debt"],
        target_cash=target_data["cash"],
        target_diluted_shares=target_data["diluted_shares"],
        median_multiples=median_multiples,
    )

    return {
        "comps": comps,
        "median_multiples": median_multiples,
        "valuation": valuation,
    }
    