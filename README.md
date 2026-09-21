# Financial Valuation Model

A Python-based financial valuation model that uses publicly available company financial data to perform discounted cash flow (DCF) and comparable company valuations.

## Overview

This project automates the process of building a company valuation from a stock ticker. Financial and market data is retrieved using `yfinance`, normalised into a consistent internal format, and passed through the valuation model.

The model currently supports:

* Historical financial analysis
* Revenue and EBIT forecasting
* Free cash flow to the firm (FCFF) forecasting
* WACC calculation using CAPM
* Discounted cash flow valuation
* Comparable company valuation
* Implied share price calculations
* Valuation comparison visualisation
* Automated unit testing

The project is designed so that data acquisition is separated from the valuation logic. This allows the model to work with different data sources without requiring changes to the underlying valuation calculations.

## Methodology

### DCF valuation

The DCF model forecasts five years of operating performance and calculates FCFF using:

* Revenue growth
* EBIT margin
* Operating tax
* Depreciation and amortisation
* Capital expenditure
* Net working capital

The forecast assumptions are derived from historical company financials and converge towards a specified terminal growth rate.

The resulting FCFF is discounted using the company's calculated WACC. A terminal value is then calculated using the perpetuity growth method to obtain an enterprise value, which is converted to an implied equity value and share price.

### Comparable company valuation

The comparable company model calculates:

* EV/EBITDA
* Price/Earnings

for a selected group of comparable companies.

Median multiples are applied to the target company's financial data to produce implied share prices.

Companies for which the required financial data cannot be retrieved are excluded from the comparable company valuation, while the DCF valuation can continue independently.

## Data

Financial and market data is retrieved using `yfinance`.

The model uses data including:

* Income statements
* Balance sheets
* Cash flow statements
* Share prices
* Beta
* Treasury yields

The data is normalised before being passed to the valuation model so that the modelling functions are independent of the external data source.

## Installation

Clone the repository and create a virtual environment:

```bash
git clone https://github.com/JontyCawkwell/financial-valuation-model.git
cd financial-valuation-model

python -m venv .venv
```

Activate the virtual environment on Windows:

```bash
.venv\Scripts\activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

## Usage

Run the model by providing a target company ticker:

```bash
python main.py KO
```

Comparable companies can optionally be supplied:

```bash
python main.py KO PEP MNST KDP
```

The model outputs the calculated WACC, enterprise value, equity value and DCF implied share price. When comparable companies are provided, their median valuation multiples and implied share prices are also displayed.

## Project Structure

```text
financial-valuation-model/
├── data/
│   └── assumptions.yaml
├── src/
│   ├── assumptions.py
│   ├── comps.py
│   ├── data_sources.py
│   ├── dcf.py
│   ├── forecasts.py
│   ├── metrics.py
│   ├── valuation.py
│   ├── visualisation.py
│   └── wacc.py
├── tests/
│   ├── test_assumptions.py
│   ├── test_comps.py
│   ├── test_dcf.py
│   ├── test_forecasts.py
│   ├── test_metrics.py
│   ├── test_valuation.py
│   └── test_wacc.py
├── .gitignore
├── main.py
├── README.md
└── requirements.txt
```

## Testing

The project uses `pytest` for automated testing.

Run the complete test suite with:

```bash
pytest
```

The tests cover the core financial calculations, including assumptions, metrics, forecasts, DCF valuation, WACC and comparable company valuation.

## Limitations

This model is intended as a personal financial modelling and programming project rather than a production investment tool.

The model relies on data retrieved from `yfinance`, and the availability and naming of financial data can vary between companies. Some companies or industries may therefore not be suitable for the current valuation framework.

The assumptions and valuation methodology are simplified and should not be treated as investment advice.

## Future Development

Potential future improvements include:

* DCF sensitivity analysis
* Additional valuation methods
* Improved handling of company-specific financial statement structures
* Additional data sources
* More detailed visualisation of forecast and valuation outputs
