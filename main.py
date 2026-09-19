from src.data import load_historical_data, validate_historical_data
from src.metrics import (
    calculate_gross_profit,
    calculate_gross_margin,
    calculate_ebit_margin,
    calculate_effective_tax_rate,
    calculate_nwc,
    calculate_nwc_to_revenue,
    calculate_free_cash_flow,
    calculate_da_to_revenue,
    calculate_capex_to_revenue,
)

data = load_historical_data()

validate_historical_data(data)

data["gross_profit"] = calculate_gross_profit(data)
data["gross_margin"] = calculate_gross_margin(data)
data["ebit_margin"] = calculate_ebit_margin(data)

print(
    data[
        [
            "year",
            "revenue",
            "gross_profit",
            "gross_margin",
            "operating_income",
            "ebit_margin",
        ]
    ]
)

data["effective_tax_rate"] = calculate_effective_tax_rate(data)
data["nwc"] = calculate_nwc(data)
data["nwc_to_revenue"] = calculate_nwc_to_revenue(data)
data["free_cash_flow"] = calculate_free_cash_flow(data)

print(data[["year", "effective_tax_rate"]])
print(data[["year", "nwc"]])
print(data[["year", "nwc", "nwc_to_revenue"]])
print(data[["year", "operating_cash_flow", "capex", "free_cash_flow"]])


data["da_to_revenue"] = calculate_da_to_revenue(data)
data["capex_to_revenue"] = calculate_capex_to_revenue(data)

print(
    data[
        [
            "year",
            "depreciation_amortisation",
            "da_to_revenue",
            "capex",
            "capex_to_revenue",
        ]
    ]
)
