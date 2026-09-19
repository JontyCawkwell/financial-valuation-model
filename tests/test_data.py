from pathlib import Path
import sys

import pandas as pd
import pytest

sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.data import load_historical_data, validate_historical_data


def test_load_historical_data():
    data = load_historical_data()

    assert isinstance(data, pd.DataFrame)
    assert not data.empty


def test_validate_historical_data():
    data = load_historical_data()

    validate_historical_data(data)


def test_validate_historical_data_missing_column():
    data = load_historical_data()
    data = data.drop(columns=["revenue"])

    with pytest.raises(
        ValueError,
        match="Missing required columns",
    ):
        validate_historical_data(data)


def test_validate_historical_data_missing_year():
    data = load_historical_data()
    data.loc[0, "year"] = None

    with pytest.raises(
        ValueError,
        match="Year column contains missing values",
    ):
        validate_historical_data(data)


def test_validate_historical_data_duplicate_year():
    data = load_historical_data()
    data.loc[len(data)] = data.iloc[-1]

    with pytest.raises(
        ValueError,
        match="Year column contains duplicate years",
    ):
        validate_historical_data(data)


def test_validate_historical_data_missing_value():
    data = load_historical_data()
    data.loc[0, "revenue"] = None

    with pytest.raises(
        ValueError,
        match="Historical data contains missing values",
    ):
        validate_historical_data(data)


def test_validate_historical_data_unsorted_years():
    data = load_historical_data()
    data = data.iloc[::-1].reset_index(drop=True)

    with pytest.raises(
        ValueError,
        match="Years must be in ascending order",
    ):
        validate_historical_data(data)