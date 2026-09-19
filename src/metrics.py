import pandas as pd


def calculate_gross_profit(data: pd.DataFrame) -> pd.Series:
    """Calculate gross profit from revenue and cost of goods sold."""
    return data["revenue"] - data["cogs"]


def calculate_gross_margin(data: pd.DataFrame) -> pd.Series:
    """Calculate gross margin as a percentage of revenue."""
    return data["gross_profit"] / data["revenue"]


def calculate_ebit_margin(data: pd.DataFrame) -> pd.Series:
    """Calculate EBIT margin as a percentage of revenue."""
    return data["operating_income"] / data["revenue"]

def calculate_pre_tax_income(data: pd.DataFrame) -> pd.Series:
    """Calculate pre-tax income from operating income and interest expense."""
    return data["operating_income"] - data["interest_expense"]


def calculate_effective_tax_rate(data: pd.DataFrame) -> pd.Series:
    """Calculate the effective tax rate from tax expense and pre-tax income."""
    pre_tax_income = calculate_pre_tax_income(data)
    return data["income_tax_expense"] / pre_tax_income


def calculate_nwc(data: pd.DataFrame) -> pd.Series:
    """Calculate net working capital from operating current assets and liabilities."""
    return (
        data["accounts_receivable"]
        + data["inventories"]
        - data["accounts_payable"]
    )


def calculate_nwc_to_revenue(data: pd.DataFrame) -> pd.Series:
    """Calculate net working capital as a proportion of revenue."""
    return data["nwc"] / data["revenue"]


def calculate_free_cash_flow(data: pd.DataFrame) -> pd.Series:
    """Calculate free cash flow from operating cash flow and capital expenditure."""
    return data["operating_cash_flow"] - data["capex"]