import pandas as pd
import requests
from typing import List, Dict
from config import settings

def calculate_monthly_averages_by_wine(raw_prices: List[Dict]) -> List[Dict]:
    if not raw_prices:
        return []
    
    df = pd.DataFrame(raw_prices)
            
    # Filter rows where price_value is not null
    df = df.dropna(subset=['price_value'])
    
    if df.empty:
        return []

    # Calculate average
    # Group by description, year, month and calculate mean of price_value
    averages_df = df.groupby(['member_state_code', 'description', 'year', 'month'])['price_value'].mean().reset_index()
    
    # Rename price_value to avg_price_value
    averages_df = averages_df.rename(columns={'price_value': 'avg_price_value'})
    
    # Convert back to list of dicts
    return averages_df.to_dict(orient='records')

def run_processing_flow() -> int:
    print("Fetching raw data from repository for pandas processing...")
    # Step 1: Get raw data
    resp = requests.get(
        f"{settings.repository_url}/prices",
        timeout=settings.request_timeout
    )
    resp.raise_for_status()
    raw_prices = resp.json()
    print(f"Fetched {len(raw_prices)} raw price records.")

    if not raw_prices:
        print("No data to process.")
        return 0

    # Step 2: Calculate averages using pandas
    averages = calculate_monthly_averages_by_wine(raw_prices)
    print(f"Calculated {len(averages)} average records using pandas.")

    if not averages:
        print("No aggregated data to save.")
        return 0

    # Step 3: Write results back to the DB via repository
    resp = requests.post(
        f"{settings.repository_url}/prices/averages/batch", 
        json=averages, 
        timeout=settings.request_timeout
    )
    resp.raise_for_status()
    inserted = resp.json().get('inserted', 0)
    print(f"Successfully saved {inserted} average records.")
    return inserted
