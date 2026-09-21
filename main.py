from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.data_sources import (
    get_company_data,
    get_market_data,
    normalise_historical_data,
)
from src.assumptions import load_assumptions
from src.forecasts import build_forecast
from src.valuation import build_valuation
from src.comps import build_comps_valuation


def main():
    ticker = "ko"

    data = get_company_data(ticker)

    historical_data = normalise_historical_data(data)
    market_data = get_market_data(data)
    assumptions = load_assumptions()

    forecast = build_forecast(
        historical_data=historical_data,
        assumptions=assumptions,
    )

    valuation = build_valuation(
        historical_data=historical_data,
        forecast=forecast,
        market_data=market_data,
        assumptions=assumptions,
    )

    comparable_tickers = [
    "PEP",
    "MNST",
    "KDP",
    ]

    comps_valuation = build_comps_valuation(
        target_historical_data=historical_data,
        comparable_tickers=comparable_tickers,
    )

    print(f"\nTicker: {ticker.upper()}")
    print("\nValuation:")
    print(f"WACC: {valuation['wacc']:.2%}")
    print(f"Enterprise value: {valuation['enterprise_value']:.2f}")
    print(f"Equity value: {valuation['equity_value']:.2f}")
    print(f"Implied share price: {valuation['implied_share_price']:.2f}")

    print("\nComparable company valuation:")

    print("\nMedian multiples:")
    print(
        f"EV/EBITDA: "
        f"{comps_valuation['median_multiples']['ev_to_ebitda']:.2f}"
    )
    print(
        f"P/E: "
        f"{comps_valuation['median_multiples']['price_to_earnings']:.2f}"
    )

    print("\nImplied share prices:")
    print(
        f"EV/EBITDA: "
        f"{comps_valuation['valuation']['implied_share_price_ev']:.2f}"
    )
    print(
        f"P/E: "
        f"{comps_valuation['valuation']['implied_share_price_pe']:.2f}"
    )
    


if __name__ == "__main__":
    main()