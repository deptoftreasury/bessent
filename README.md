# Bessent

Bessent is a Python client for interacting with U.S. Department of Treasury APIs.

## Features

- Daily Treasury yield curve rates
- U.S. debt to the penny data
- Monthly Treasury Statement information
- Treasury exchange rates for major currencies

## Installation

Install the required dependencies:

```bash
pip install requests pandas
```

## Usage

Run the program:

```bash
python bessent.py
```

The program will automatically fetch and display:
- Latest Treasury interest rates (1-month to 30-year)
- Recent national debt figures
- Exchange rates for EUR, GBP, JPY, and CAD
- Monthly Treasury Statement highlights

## API Methods

### TreasuryAPIClient

- `get_daily_treasury_rates(date, limit)` - Fetch Treasury yield curve rates
- `get_debt_to_penny(start_date, end_date)` - Get national debt data
- `get_monthly_treasury_statement(year, month)` - Retrieve monthly financial summaries
- `get_exchange_rates(currency, date)` - Get official exchange rates

### Parameters

- **date**: Date in YYYY-MM-DD format
- **limit**: Number of records to return
- **currency**: Currency code (EUR, GBP, JPY, etc.)
- **year/month**: Specific year and month for data

## Example Output

```
Bessent - Treasury API Client
===============================

1. Fetching latest Treasury rates...

============================================================
DAILY TREASURY YIELD CURVE RATES
============================================================

Date: 2025-06-04
------------------------------
1 Month     : 4.15%
3 Month     : 4.28%
6 Month     : 4.35%
1 Year      : 4.42%
2 Year      : 4.58%
5 Year      : 4.75%
10 Year     : 4.89%
30 Year     : 5.12%
```

## Data Sources

All data is retrieved from official U.S. Treasury APIs:
- Treasury Fiscal Data API
- Daily Treasury Yield Curve Rates
- Debt to the Penny
- Monthly Treasury Statement
- Treasury Reporting Rates of Exchange

## Requirements

- Python 3.6+
- requests
- pandas

## Author

Michael Mendy (c) 2025. 
