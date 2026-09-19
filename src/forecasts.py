import pandas as pd


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
