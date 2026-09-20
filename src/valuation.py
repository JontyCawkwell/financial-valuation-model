from pathlib import Path
import sys

import pandas as pd


sys.path.append(str(Path(__file__).resolve().parent.parent))
from src.wacc import build_wacc
from src.dcf import (
    build_dcf,
    calculate_equity_value,
    calculate_implied_share_price,
)



def build_valuation(
    historical_data: pd.DataFrame,
    forecast: pd.DataFrame,
    assumptions: dict,
) -> dict:
    """Build a complete DCF valuation from historical and forecast data."""

    wacc = build_wacc(
        historical_data=historical_data,
        assumptions=assumptions,
    )

    dcf_result = build_dcf(
        forecast=forecast,
        wacc=wacc,
        terminal_growth_rate=assumptions["terminal"]["growth_rate"],
    )

    latest = historical_data.iloc[-1]

    debt = (
        latest["short_term_debt"]
        + latest["long_term_debt"]
    )

    cash = latest["cash"]
    diluted_shares = latest["diluted_shares"]

    equity_value = calculate_equity_value(
        enterprise_value=dcf_result["enterprise_value"],
        debt=debt,
        cash=cash,
    )

    implied_share_price = calculate_implied_share_price(
        equity_value=equity_value,
        diluted_shares=diluted_shares,
    )

    return {
        "wacc": wacc,
        "enterprise_value": dcf_result["enterprise_value"],
        "equity_value": equity_value,
        "implied_share_price": implied_share_price,
    }