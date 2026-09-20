import pandas as pd
import yfinance as yf
from pathlib import Path
import sys

from src.data_sources import (
    get_company_data,
    extract_revenue,
    extract_operating_income,
    extract_tax,
    extract_diluted_shares,
    extract_cash,
    extract_accounts_receivable,
    extract_inventory,
    extract_accounts_payable,
    extract_capex,
    extract_depreciation_amortisation,
)


EXTRACTORS = {
    "revenue": extract_revenue,
    "operating_income": extract_operating_income,
    "tax": extract_tax,
    "diluted_shares": extract_diluted_shares,
    "cash": extract_cash,
    "accounts_receivable": extract_accounts_receivable,
    "inventory": extract_inventory,
    "accounts_payable": extract_accounts_payable,
    "capex": extract_capex,
    "depreciation_amortisation": extract_depreciation_amortisation,
}


def get_sp500_tickers():
    """Get the current S&P 500 constituent tickers."""

    table = pd.read_html(
        "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    )[0]

    return table["Symbol"].str.replace(".", "-", regex=False).tolist()


def test_ticker(ticker):
    """Test all required data fields for one ticker."""

    try:
        data = get_company_data(ticker)

    except Exception as error:
        return {
            "ticker": ticker,
            "status": "DATA ERROR",
            "field": "company_data",
            "error": str(error),
        }

    statements = {
        "revenue": data["income_statement"],
        "operating_income": data["income_statement"],
        "tax": data["income_statement"],
        "diluted_shares": data["income_statement"],
        "cash": data["balance_sheet"],
        "accounts_receivable": data["balance_sheet"],
        "inventory": data["balance_sheet"],
        "accounts_payable": data["balance_sheet"],
        "capex": data["cash_flow"],
        "depreciation_amortisation": data["cash_flow"],
    }

    for field, extractor in EXTRACTORS.items():
        try:
            extractor(statements[field])

        except Exception as error:
            return {
                "ticker": ticker,
                "status": "FAIL",
                "field": field,
                "error": str(error),
            }

    return {
        "ticker": ticker,
        "status": "PASS",
        "field": "",
        "error": "",
    }


def main():
    tickers = get_sp500_tickers()

    print(f"Testing {len(tickers)} S&P 500 companies...\n")

    results = []

    for number, ticker in enumerate(tickers, start=1):
        result = test_ticker(ticker)
        results.append(result)

        if result["status"] == "PASS":
            print(f"[{number}/{len(tickers)}] {ticker}: PASS")
        else:
            print(
                f"[{number}/{len(tickers)}] "
                f"{ticker}: {result['status']} - {result['field']}"
            )

    results = pd.DataFrame(results)

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    print(f"Total companies: {len(results)}")
    print(
        f"Passed: {(results['status'] == 'PASS').sum()}"
    )
    print(
        f"Failed: {(results['status'] == 'FAIL').sum()}"
    )
    print(
        f"Data errors: {(results['status'] == 'DATA ERROR').sum()}"
    )

    failures = results[results["status"] != "PASS"]

    if not failures.empty:
        print("\nFAILURES BY FIELD")
        print("-" * 60)

        field_counts = (
            failures["field"]
            .value_counts()
        )

        print(field_counts)

        print("\nDETAILED FAILURES")
        print("-" * 60)

        print(
            failures[
                ["ticker", "status", "field", "error"]
            ].to_string(index=False)
        )

    results.to_csv(
        "tests/sp500_data_source_results.csv",
        index=False,
    )

    print(
        "\nFull results saved to "
        "tests/sp500_data_source_results.csv"
    )


if __name__ == "__main__":
    main()