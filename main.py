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


def main():
    ticker = "KO"

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

    print(f"Company: {ticker}")

    print("\nMarket data:")
    print(market_data)

    print("\nForecast:")
    print(forecast)

    print("\nValuation:")
    print(f"WACC: {valuation['wacc']:.2%}")
    print(f"Enterprise value: {valuation['enterprise_value']:.2f}")
    print(f"Equity value: {valuation['equity_value']:.2f}")
    print(
        f"Implied share price: "
        f"{valuation['implied_share_price']:.2f}"
    )


if __name__ == "__main__":
    main()