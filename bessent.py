#!/usr/bin/env python3

import requests
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import pandas as pd

class TreasuryAPIClient:
    
    def __init__(self):
        self.base_urls = {
            'fiscal_data': 'https://api.fiscaldata.treasury.gov/services/api/fiscal_service',
            'treasury_rates': 'https://api.fiscaldata.treasury.gov/services/api/fiscal_service'
        }
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Treasury-API-Client/1.0',
            'Accept': 'application/json'
        })
    
    def get_daily_treasury_rates(self, date: str = None, limit: int = 100) -> Dict:
        endpoint = f"{self.base_urls['treasury_rates']}/v1/accounting/od/avg_interest_rates"
        
        params = {
            'limit': limit,
            'sort': '-record_date'
        }
        
        if date:
            params['filter'] = f'record_date:eq:{date}'
        
        try:
            response = self.session.get(endpoint, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching treasury rates: {e}")
            return {}
    
    def get_debt_to_penny(self, start_date: str = None, end_date: str = None) -> Dict:
        endpoint = f"{self.base_urls['fiscal_data']}/v1/accounting/od/debt_to_penny"
        
        params = {
            'limit': 1000,
            'sort': '-record_date'
        }
        
        filters = []
        if start_date:
            filters.append(f'record_date:gte:{start_date}')
        if end_date:
            filters.append(f'record_date:lte:{end_date}')
        
        if filters:
            params['filter'] = ','.join(filters)
        
        try:
            response = self.session.get(endpoint, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching debt data: {e}")
            return {}
    
    def get_monthly_treasury_statement(self, year: int = None, month: int = None) -> Dict:
        endpoint = f"{self.base_urls['fiscal_data']}/v1/accounting/mts/mts_table_1"
        
        if not year:
            year = datetime.now().year
        if not month:
            month = datetime.now().month
        
        date_filter = f"{year}-{month:02d}"
        
        params = {
            'filter': f'record_date:like:{date_filter}',
            'limit': 100
        }
        
        try:
            response = self.session.get(endpoint, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching treasury statement: {e}")
            return {}
    
    def get_exchange_rates(self, currency: str = None, date: str = None) -> Dict:
        endpoint = f"{self.base_urls['fiscal_data']}/v1/accounting/od/rates_of_exchange"
        
        params = {
            'limit': 200,
            'sort': '-record_date'
        }
        
        filters = []
        if currency:
            filters.append(f'currency:eq:{currency.upper()}')
        if date:
            filters.append(f'record_date:eq:{date}')
        
        if filters:
            params['filter'] = ','.join(filters)
        
        try:
            response = self.session.get(endpoint, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching exchange rates: {e}")
            return {}

def format_currency(amount: str) -> str:
    try:
        value = float(amount.replace(',', ''))
        return f"${value:,.2f}"
    except (ValueError, AttributeError):
        return amount

def display_treasury_rates(data: Dict):
    if not data or 'data' not in data:
        print("No treasury rate data available")
        return
    
    print("\n" + "="*60)
    print("DAILY TREASURY YIELD CURVE RATES")
    print("="*60)
    
    for record in data['data'][:10]:
        date = record.get('record_date', 'N/A')
        print(f"\nDate: {date}")
        print("-" * 30)
        
        rate_fields = ['1_month', '3_month', '6_month', '1_year', '2_year', '5_year', '10_year', '30_year']
        for field in rate_fields:
            if field in record and record[field]:
                rate_name = field.replace('_', ' ').title()
                print(f"{rate_name:12}: {record[field]}%")

def display_debt_data(data: Dict):
    if not data or 'data' not in data:
        print("No debt data available")
        return
    
    print("\n" + "="*60)
    print("U.S. DEBT TO THE PENNY")
    print("="*60)
    
    for record in data['data'][:5]:
        date = record.get('record_date', 'N/A')
        total_debt = record.get('tot_pub_debt_out_amt', 'N/A')
        
        print(f"\nDate: {date}")
        print(f"Total Public Debt: {format_currency(total_debt)}")

def main():
    print("Bessent - Treasury API Client")
    print("===============================")
    
    client = TreasuryAPIClient()
    
    today = datetime.now()
    last_week = today - timedelta(days=7)
    
    try:
        print("\n1. Fetching latest Treasury rates...")
        rates_data = client.get_daily_treasury_rates(limit=5)
        display_treasury_rates(rates_data)
        
        print("\n2. Fetching recent debt data...")
        debt_data = client.get_debt_to_penny(
            start_date=last_week.strftime('%Y-%m-%d'),
            end_date=today.strftime('%Y-%m-%d')
        )
        display_debt_data(debt_data)
        
        print("\n3. Fetching exchange rates...")
        currencies = ['EUR', 'GBP', 'JPY', 'CAD']
        
        print("\n" + "="*60)
        print("TREASURY EXCHANGE RATES")
        print("="*60)
        
        for currency in currencies:
            exchange_data = client.get_exchange_rates(currency=currency)
            if exchange_data and 'data' in exchange_data and exchange_data['data']:
                latest_rate = exchange_data['data'][0]
                date = latest_rate.get('record_date', 'N/A')
                rate = latest_rate.get('exchange_rate', 'N/A')
                print(f"{currency}/USD: {rate} (as of {date})")
        
        print("\n4. Fetching Monthly Treasury Statement...")
        mts_data = client.get_monthly_treasury_statement()
        
        if mts_data and 'data' in mts_data:
            print("\n" + "="*60)
            print("MONTHLY TREASURY STATEMENT (Latest)")
            print("="*60)
            
            if mts_data['data']:
                latest_mts = mts_data['data'][0]
                print(f"Date: {latest_mts.get('record_date', 'N/A')}")
                print(f"Classification: {latest_mts.get('classification_desc', 'N/A')}")
                print(f"Current Month: {format_currency(latest_mts.get('current_month_net_amt', '0'))}")
                print(f"Fiscal YTD: {format_currency(latest_mts.get('fiscal_year_to_date_net_amt', '0'))}")
        
    except Exception as e:
        print(f"An error occurred: {e}")
    
    print("\n" + "="*60)
    print("API Documentation: https://fiscaldata.treasury.gov/api-documentation/")
    print("="*60)

if __name__ == "__main__":
    main()
