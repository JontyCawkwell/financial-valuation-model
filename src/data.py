from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "historical_financials.csv"

REQUIRED_COLUMNS = [
    "year",
    "revenue",
    "cogs",
    "operating_income",
    "interest_expense",
    "income_tax_expense",
    "net_income",
    "diluted_shares",
    "cash",
    "short_term_debt",
    "long_term_debt",
    "accounts_receivable",
    "inventories",
    "accounts_payable",
    "goodwill",
    "equity_method_investments",
    "shareholders_equity",
    "operating_cash_flow",
    "capex",
    "depreciation_amortisation",
]


def load_historical_data(path: Path = DATA_PATH) -> pd.DataFrame:
    """Load historical financial data from the project data directory."""
    return pd.read_csv(path)


def validate_historical_data(data: pd.DataFrame) -> None:
    """Validate the structure and contents of historical financial data."""

    missing_columns = set(REQUIRED_COLUMNS) - set(data.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {sorted(missing_columns)}"
        )

    if data["year"].isna().any():
        raise ValueError("Year column contains missing values.")

    if data["year"].duplicated().any():
        raise ValueError("Year column contains duplicate years.")

    if data[REQUIRED_COLUMNS].isna().any().any():
        raise ValueError("Historical data contains missing values.")

    if not data["year"].is_monotonic_increasing:
        raise ValueError("Years must be in ascending order.")