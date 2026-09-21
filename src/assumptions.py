from pathlib import Path

import yaml


PROJECT_ROOT = Path(__file__).resolve().parent.parent
ASSUMPTIONS_PATH = PROJECT_ROOT / "data" / "assumptions.yaml"


def load_assumptions(path: Path = ASSUMPTIONS_PATH) -> dict:
    """Load valuation assumptions from a YAML file."""
    with open(path, "r") as file:
        return yaml.safe_load(file)


def calculate_historical_average(data, column):
    return data[column].mean()


def calculate_historical_growth(data, column):
    growth = data[column].pct_change().dropna()
    return growth.mean()


def calculate_historical_margin(data, numerator, denominator):
    return (data[numerator] / data[denominator]).mean()


def calculate_historical_tax_rate(data):
    return (
        data["income_tax_expense"] / data["pretax_income"]
    ).mean()


def build_historical_assumptions(historical_data):
    return {
        "revenue_growth": calculate_historical_growth(
            historical_data, "revenue"
        ),
        "ebit_margin": calculate_historical_margin(
            historical_data,
            "operating_income",
            "revenue",
        ),
        "tax_rate": calculate_historical_tax_rate(
            historical_data
        ),
        "da_to_revenue": calculate_historical_margin(
            historical_data,
            "depreciation_amortisation",
            "revenue",
        ),
        "capex_to_revenue": calculate_historical_margin(
            historical_data,
            "capex",
            "revenue",
        ),
    }


def build_forecast_assumptions(
    historical_data,
    assumptions,
):
    historical_assumptions = build_historical_assumptions(
        historical_data
    )

    assumptions["forecast"] = {}

    forecast_assumptions = assumptions["forecast"]

    start_growth = historical_assumptions["revenue_growth"]
    terminal_growth = assumptions["terminal"]["growth_rate"]

    ebit_margin = historical_assumptions["ebit_margin"]
    tax_rate = historical_assumptions["tax_rate"]

    forecast_years = range(2026, 2031)

    start_year = forecast_years[0]
    end_year = forecast_years[-1]

    forecast_assumptions["revenue_growth"] = {}
    forecast_assumptions["ebit_margin"] = {}

    for year in forecast_years:
        forecast_assumptions["revenue_growth"][year] = (
            start_growth
            + (terminal_growth - start_growth)
            * (year - start_year)
            / (end_year - start_year)
        )

        forecast_assumptions["ebit_margin"][year] = ebit_margin

    forecast_assumptions["tax_rate"] = tax_rate

    return assumptions