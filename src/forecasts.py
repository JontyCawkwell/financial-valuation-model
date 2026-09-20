from pathlib import Path
import sys

import pandas as pd

sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.metrics import (
    calculate_capex_to_revenue,
    calculate_da_to_revenue,
    calculate_nwc,
    calculate_nwc_to_revenue,
)


def forecast_revenue(previous_revenue: float, growth_rate: float) -> float:
    """Forecast revenue for the next year using an assumed growth rate."""
    return previous_revenue * (1 + growth_rate)


def forecast_ebit(forecast_revenue: float, ebit_margin: float) -> float:
    """Forecast EBIT using projected revenue and an assumed EBIT margin."""
    return forecast_revenue * ebit_margin


def forecast_tax(ebit: float, tax_rate: float) -> float:
    """Forecast operating tax expense using EBIT and an assumed tax rate."""
    return ebit * tax_rate


def calculate_nopat(ebit: float, tax: float) -> float:
    """Calculate net operating profit after tax."""
    return ebit - tax


def forecast_da(forecast_revenue: float, da_to_revenue: float) -> float:
    """Forecast depreciation and amortisation as a proportion of revenue."""
    return forecast_revenue * da_to_revenue


def forecast_capex(forecast_revenue: float, capex_to_revenue: float) -> float:
    """Forecast capital expenditure as a proportion of revenue."""
    return forecast_revenue * capex_to_revenue


def forecast_nwc(forecast_revenue: float, nwc_to_revenue: float) -> float:
    """Forecast net working capital as a proportion of revenue."""
    return forecast_revenue * nwc_to_revenue


def calculate_change_in_nwc(
    current_nwc: float,
    previous_nwc: float,
) -> float:
    """Calculate the change in net working capital between two periods."""
    return current_nwc - previous_nwc


def build_forecast(
    historical_data: pd.DataFrame,
    assumptions: dict,
) -> pd.DataFrame:
    """Build a forecast of operating performance and free cash flow."""

    historical_data = historical_data.copy()
    historical_data["nwc"] = calculate_nwc(historical_data)

    forecast_assumptions = assumptions["forecast"]
    forecast_years = sorted(forecast_assumptions["revenue_growth"])

    da_to_revenue = calculate_da_to_revenue(historical_data).iloc[-1]
    capex_to_revenue = calculate_capex_to_revenue(historical_data).iloc[-1]
    nwc_to_revenue = calculate_nwc_to_revenue(historical_data).iloc[-1]

    previous_revenue = historical_data.iloc[-1]["revenue"]
    previous_nwc = historical_data.iloc[-1]["nwc"]

    forecast = []

    for year in forecast_years:
        revenue_growth = forecast_assumptions["revenue_growth"][year]
        ebit_margin = forecast_assumptions["ebit_margin"][year]
        tax_rate = forecast_assumptions["tax_rate"]

        revenue = forecast_revenue(previous_revenue, revenue_growth)
        ebit = forecast_ebit(revenue, ebit_margin)
        tax = forecast_tax(ebit, tax_rate)
        nopat = calculate_nopat(ebit, tax)

        da = forecast_da(revenue, da_to_revenue)
        capex = forecast_capex(revenue, capex_to_revenue)
        nwc = forecast_nwc(revenue, nwc_to_revenue)

        change_in_nwc = calculate_change_in_nwc(
            nwc,
            previous_nwc,
        )

        fcff = (
            nopat
            + da
            - capex
            - change_in_nwc
        )

        forecast.append(
            {
                "year": year,
                "revenue": revenue,
                "ebit": ebit,
                "tax": tax,
                "nopat": nopat,
                "da": da,
                "capex": capex,
                "nwc": nwc,
                "change_in_nwc": change_in_nwc,
                "fcff": fcff,
            }
        )

        previous_revenue = revenue
        previous_nwc = nwc

    return pd.DataFrame(forecast)