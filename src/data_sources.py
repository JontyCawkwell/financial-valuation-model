import pandas as pd
import yfinance as yf
from pathlib import Path
import sys


sys.path.append(str(Path(__file__).resolve().parent.parent))


def get_company_data(ticker: str):
    """Retrieve raw financial and market data for a company."""

    company = yf.Ticker(ticker)

    return {
        "ticker": ticker.upper(),
        "income_statement": company.income_stmt,
        "balance_sheet": company.balance_sheet,
        "cash_flow": company.cashflow,
        "info": company.info,
    }


def get_field(data, field_names: list[str]):
    """Return the first available field from a list of candidate fields."""

    for field_name in field_names:
        if field_name in data.index:
            return data.loc[field_name]

    raise KeyError(
        f"Could not find any of these fields: {field_names}"
    )


def extract_revenue(income_statement):
    return get_field(
        income_statement,
        ["Total Revenue", "Operating Revenue"],
    )


def extract_operating_income(income_statement):
    return get_field(
        income_statement,
        ["Operating Income", "EBIT"],
    )


def extract_ebitda(income_statement):
    return get_field(
        income_statement,
        ["EBITDA"],
    )


def extract_net_income(income_statement):
    return get_field(
        income_statement,
        ["Net Income"],
    )


def extract_tax(income_statement):
    return get_field(
        income_statement,
        ["Tax Provision"],
    )


def extract_diluted_shares(income_statement):
    return get_field(
        income_statement,
        ["Diluted Average Shares"],
    )


def extract_cash(balance_sheet):
    return get_field(
        balance_sheet,
        ["Cash And Cash Equivalents"],
    )


def extract_total_debt(balance_sheet):
    return get_field(
        balance_sheet,
        ["Total Debt"],
    )


def extract_accounts_receivable(balance_sheet):
    return get_field(
        balance_sheet,
        ["Accounts Receivable"],
    )


def extract_inventory(balance_sheet):
    """Extract inventory, using zero when no inventory is reported."""

    for field_name in ["Inventory", "Inventories"]:
        if field_name in balance_sheet.index:
            return balance_sheet.loc[field_name]

    return pd.Series(
        0.0,
        index=balance_sheet.columns,
    )


def extract_accounts_payable(balance_sheet):
    return get_field(
        balance_sheet,
        ["Accounts Payable", "Payables", "Payables And Accrued Expenses"],
    )


def extract_depreciation_amortisation(cash_flow):
    return get_field(
        cash_flow,
        [
            "Depreciation And Amortization",
            "Depreciation Amortization Depletion",
        ],
    )


def extract_capex(cash_flow):
    return -get_field(
        cash_flow,
        ["Capital Expenditure"],
    )


def extract_share_price(info):
    if "currentPrice" not in info:
        raise KeyError("Could not find current share price.")

    return info["currentPrice"]


def normalise_historical_data(data):
    """Convert yfinance data into the model's standard format."""

    income_statement = data["income_statement"]
    balance_sheet = data["balance_sheet"]
    cash_flow = data["cash_flow"]

    historical_data = {
        "revenue": extract_revenue(income_statement),
        "operating_income": extract_operating_income(income_statement),
        "ebitda": extract_ebitda(income_statement),
        "net_income": extract_net_income(income_statement),
        "income_tax_expense": extract_tax(income_statement),
        "diluted_shares": extract_diluted_shares(income_statement),
        "cash": extract_cash(balance_sheet),
        "total_debt": extract_total_debt(balance_sheet),
        "accounts_receivable": extract_accounts_receivable(balance_sheet),
        "inventories": extract_inventory(balance_sheet),
        "accounts_payable": extract_accounts_payable(balance_sheet),
        "capex": extract_capex(cash_flow),
        "depreciation_amortisation": extract_depreciation_amortisation(
            cash_flow
        ),
    }

    historical_data = pd.DataFrame(historical_data)

    historical_data.index = historical_data.index.year
    historical_data.index.name = "year"

    historical_data = historical_data.sort_index()
    historical_data = historical_data.dropna()

    return historical_data.reset_index()


def get_market_data(data):
    """Extract current market data separately from historical financial data."""

    info = data["info"]

    return {
        "ticker": data["ticker"],
        "share_price": extract_share_price(info),
    }


if __name__ == "__main__":
    data = get_company_data("AAPL")

    historical_data = normalise_historical_data(data)
    market_data = get_market_data(data)

    print(historical_data)
    print(market_data)