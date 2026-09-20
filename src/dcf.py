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