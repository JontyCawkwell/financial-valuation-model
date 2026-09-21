from pathlib import Path
import sys

import argparse

sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.data_sources import (
    get_company_data,
    get_market_data,
    normalise_historical_data,
)
from src.assumptions import (
    load_assumptions,
    build_historical_assumptions,
    build_forecast_assumptions
)
from src.forecasts import build_forecast
from src.valuation import build_valuation
from src.comps import build_comps_valuation


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Run a DCF and comparable company valuation."
    )

    parser.add_argument(
        "target",
        help="Target company ticker."
    )

    parser.add_argument(
        "comps",
        nargs="*",
        help="Comparable company tickers."
    )

    return parser.parse_args()


def main(target_ticker, comparable_tickers):
    ticker = target_ticker.upper()
    try:
        data = get_company_data(ticker)

        historical_data = normalise_historical_data(data)
        market_data = get_market_data(data)

    except Exception:
        print(
            f"\nError: Required financial data could not be retrieved for "
            f"{ticker.upper()}."
        )
        print(
            "The DCF valuation cannot be calculated because the target "
            "company's financial data is required for the model."
        )
        print(
            "Some industries, such as banks and other financial institutions, "
            "may not be suitable for this valuation model."
        )
        print(
            "The valuation has been stopped."
        )
        return

    assumptions = build_forecast_assumptions(
        historical_data=historical_data,
        assumptions=load_assumptions(),
        )

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

    comps_valuation = None
    if not comparable_tickers:
        print(
            "\nNo comparable companies were provided."
        )
        print(
            "Comparable company valuation has been skipped."
        )
    else:
        comps_valuation = build_comps_valuation(
            target_historical_data=historical_data,
            comparable_tickers=comparable_tickers,
        )

    print(f"\n{ticker.upper()} Valuation")
    print("-" * 30)

    print(f"Current share price:  ${market_data['share_price']:.2f}")
    print(f"WACC:                 {valuation['wacc']:.2%}")
    print(
        f"Enterprise value:     "
        f"${valuation['enterprise_value'] / 1e9:.2f}bn"
    )
    print(
        f"Equity value:         "
        f"${valuation['equity_value'] / 1e9:.2f}bn"
    )
    print(f"DCF implied price:    ${valuation['implied_share_price']:.2f}")

    if comps_valuation is not None:
        print("\nComparable Company Valuation")
        print("-" * 30)

        print(
            f"Median EV/EBITDA:     "
            f"{comps_valuation['median_multiples']['ev_to_ebitda']:.2f}x"
        )
        print(
            f"Median P/E:           "
            f"{comps_valuation['median_multiples']['price_to_earnings']:.2f}x"
        )
        print(
            f"EV/EBITDA price:      "
            f"${comps_valuation['valuation']['implied_share_price_ev']:.2f}"
        )
        print(
            f"P/E price:            "
            f"${comps_valuation['valuation']['implied_share_price_pe']:.2f}"
        )

if __name__ == "__main__":
    args = parse_arguments()
    main(
        target_ticker=args.target,
        comparable_tickers=args.comps,
    )