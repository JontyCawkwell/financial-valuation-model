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


def calculate_market_value_equity(
    share_price: float,
    diluted_shares: float,
) -> float:
    """Calculate market value of equity from share price and diluted shares."""
    return share_price * diluted_shares


def calculate_total_debt(
    short_term_debt: float,
    long_term_debt: float,
) -> float:
    """Calculate total debt from short-term and long-term debt."""
    return short_term_debt + long_term_debt


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


def build_wacc(
    historical_data,
    market_data,
    assumptions: dict,
) -> float:
    """Calculate WACC using historical and market data."""

    latest = historical_data.iloc[-1]
    wacc_assumptions = assumptions["wacc"]

    market_value_equity = calculate_market_value_equity(
        share_price=market_data["share_price"],
        diluted_shares=latest["diluted_shares"],
    )

    debt = latest["total_debt"]

    cost_of_equity = calculate_cost_of_equity(
        risk_free_rate=wacc_assumptions["risk_free_rate"],
        beta=wacc_assumptions["beta"],
        market_risk_premium=wacc_assumptions["market_risk_premium"],
    )

    return calculate_wacc(
        market_value_equity=market_value_equity,
        debt=debt,
        cost_of_equity=cost_of_equity,
        cost_of_debt=wacc_assumptions["cost_of_debt"],
        tax_rate=wacc_assumptions["tax_rate"],
    )