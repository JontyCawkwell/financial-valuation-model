import pandas as pd


def calculate_ev_to_ebitda(
    enterprise_value: float,
    ebitda: float,
) -> float:
    """Calculate the enterprise value to EBITDA multiple."""
    return enterprise_value / ebitda


def calculate_price_to_earnings(
    equity_value: float,
    net_income: float,
) -> float:
    """Calculate the price to earnings multiple."""
    return equity_value / net_income


def calculate_implied_enterprise_value(
    ebitda: float,
    ev_to_ebitda: float,
) -> float:
    """Calculate implied enterprise value from an EV/EBITDA multiple."""
    return ebitda * ev_to_ebitda


def calculate_implied_equity_value(
    net_income: float,
    price_to_earnings: float,
) -> float:
    """Calculate implied equity value from a P/E multiple."""
    return net_income * price_to_earnings