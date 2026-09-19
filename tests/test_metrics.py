from pathlib import Path
import sys

import pandas as pd
import pytest

sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.metrics import (
    calculate_capex_to_revenue,
    calculate_da_to_revenue,
    calculate_ebit_margin,
    calculate_effective_tax_rate,
    calculate_free_cash_flow,
    calculate_gross_margin,
    calculate_gross_profit,
    calculate_nwc,
    calculate_nwc_to_revenue,
    calculate_pre_tax_income,
)


def test_calculate_gross_profit():
    data = pd.DataFrame({
        "revenue": [100],
        "cogs": [40],
    })

    assert calculate_gross_profit(data).iloc[0] == pytest.approx(60)


def test_calculate_gross_margin():
    data = pd.DataFrame({
        "revenue": [100],
        "gross_profit": [60],
    })

    assert calculate_gross_margin(data).iloc[0] == pytest.approx(0.60)


def test_calculate_ebit_margin():
    data = pd.DataFrame({
        "revenue": [100],
        "operating_income": [20],
    })

    assert calculate_ebit_margin(data).iloc[0] == pytest.approx(0.20)


def test_calculate_pre_tax_income():
    data = pd.DataFrame({
        "operating_income": [20],
        "interest_expense": [5],
    })

    assert calculate_pre_tax_income(data).iloc[0] == pytest.approx(15)


def test_calculate_effective_tax_rate():
    data = pd.DataFrame({
        "operating_income": [20],
        "interest_expense": [5],
        "income_tax_expense": [3],
    })

    assert calculate_effective_tax_rate(data).iloc[0] == pytest.approx(0.20)


def test_calculate_nwc():
    data = pd.DataFrame({
        "accounts_receivable": [30],
        "inventories": [20],
        "accounts_payable": [10],
    })

    assert calculate_nwc(data).iloc[0] == pytest.approx(40)


def test_calculate_nwc_to_revenue():
    data = pd.DataFrame({
        "nwc": [40],
        "revenue": [100],
    })

    assert calculate_nwc_to_revenue(data).iloc[0] == pytest.approx(0.40)


def test_calculate_free_cash_flow():
    data = pd.DataFrame({
        "operating_cash_flow": [50],
        "capex": [10],
    })

    assert calculate_free_cash_flow(data).iloc[0] == pytest.approx(40)


def test_calculate_da_to_revenue():
    data = pd.DataFrame({
        "depreciation_amortisation": [8],
        "revenue": [100],
    })

    assert calculate_da_to_revenue(data).iloc[0] == pytest.approx(0.08)


def test_calculate_capex_to_revenue():
    data = pd.DataFrame({
        "capex": [10],
        "revenue": [100],
    })

    assert calculate_capex_to_revenue(data).iloc[0] == pytest.approx(0.10)