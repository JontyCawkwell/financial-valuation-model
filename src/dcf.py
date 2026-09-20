import pandas as pd


def calculate_fcff(
    nopat: float,
    depreciation_amortisation: float,
    capex: float,
    change_in_nwc: float,
) -> float:
    """Calculate free cash flow to the firm."""
    return (
        nopat
        + depreciation_amortisation
        - capex
        - change_in_nwc
    )


def discount_cash_flow(
    cash_flow: float,
    discount_rate: float,
    period: int,
) -> float:
    """Discount a future cash flow to its present value."""
    return cash_flow / (1 + discount_rate) ** period


def calculate_terminal_value_perpetuity(
    final_fcff: float,
    wacc: float,
    terminal_growth_rate: float,
) -> float:
    """Calculate terminal value using the perpetual growth method."""
    return (
        final_fcff * (1 + terminal_growth_rate)
        / (wacc - terminal_growth_rate)
    )


def calculate_terminal_value_exit_multiple(
    final_ebitda: float,
    exit_multiple: float,
) -> float:
    """Calculate terminal value using an exit multiple."""
    return final_ebitda * exit_multiple


def build_dcf(
    forecast: pd.DataFrame,
    wacc: float,
    terminal_growth_rate: float,
) -> dict:
    """Build a DCF valuation using the perpetual growth method."""

    discounted_fcff = []

    for period, fcff in enumerate(forecast["fcff"], start=1):
        discounted_fcff.append(
            discount_cash_flow(
                cash_flow=fcff,
                discount_rate=wacc,
                period=period,
            )
        )

    terminal_value = calculate_terminal_value_perpetuity(
        final_fcff=forecast.iloc[-1]["fcff"],
        wacc=wacc,
        terminal_growth_rate=terminal_growth_rate,
    )

    discounted_terminal_value = discount_cash_flow(
        cash_flow=terminal_value,
        discount_rate=wacc,
        period=len(forecast),
    )

    enterprise_value = (
        sum(discounted_fcff)
        + discounted_terminal_value
    )

    return {
        "discounted_fcff": discounted_fcff,
        "terminal_value": terminal_value,
        "discounted_terminal_value": discounted_terminal_value,
        "enterprise_value": enterprise_value,
    }


def calculate_equity_value(
    enterprise_value: float,
    debt: float,
    cash: float,
) -> float:
    """Calculate equity value from enterprise value, debt, and cash."""
    return enterprise_value - debt + cash


def calculate_implied_share_price(
    equity_value: float,
    diluted_shares: float,
) -> float:
    """Calculate implied share price from equity value and diluted shares."""
    return equity_value / diluted_shares