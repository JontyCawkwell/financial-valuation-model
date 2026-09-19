def calculate_cost_of_equity(
    risk_free_rate: float,
    beta: float,
    market_risk_premium: float,
) -> float:
    """Calculate cost of equity using the CAPM."""
    return risk_free_rate + beta * market_risk_premium


def calculate_after_tax_cost_of_debt(
    cost_of_debt: float,
    tax_rate: float,
) -> float:
    """Calculate the after-tax cost of debt."""
    return cost_of_debt * (1 - tax_rate)


def calculate_wacc(
    market_value_equity: float,
    debt: float,
    cost_of_equity: float,
    cost_of_debt: float,
    tax_rate: float,
) -> float:
    """Calculate weighted average cost of capital."""

    total_capital = market_value_equity + debt

    equity_weight = market_value_equity / total_capital
    debt_weight = debt / total_capital

    after_tax_cost_of_debt = calculate_after_tax_cost_of_debt(
        cost_of_debt,
        tax_rate,
    )

    return (
        equity_weight * cost_of_equity
        + debt_weight * after_tax_cost_of_debt
    )