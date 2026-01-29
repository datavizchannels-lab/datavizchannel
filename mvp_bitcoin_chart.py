#!/usr/bin/env python3
"""
MVP Script: Bitcoin Price Chart Generator
Gets Bitcoin price from CoinGecko and generates a 7-day sparkline chart
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.coingecko_api import CoingeckoAPI
from src.chart_generator import QuickChartGenerator

def main():
    print("🚀 Starting Bitcoin Chart Generator MVP...")
    
    # Initialize APIs
    coingecko = CoingeckoAPI()
    chart_generator = QuickChartGenerator()
    
    # Get Bitcoin market data
    print("📊 Fetching Bitcoin data...")
    markets = coingecko.get_coin_markets(per_page=1, sparkline=False)
    
    if not markets or len(markets) == 0:
        print("❌ Failed to fetch Bitcoin data")
        return False
    
    bitcoin = markets[0]
    print(f"✅ Bitcoin data retrieved:")
    print(f"   Price: ${bitcoin['current_price']:,.2f}")
    print(f"   24h Change: {bitcoin['price_change_percentage_24h']:.2f}%")
    
    # Get 7-day price history
    print("📈 Fetching 7-day price history...")
    sparkline_data = coingecko.get_coin_price_history('bitcoin', days=7)
    
    if not sparkline_data:
        print("❌ No price history data available")
        return False
    
    print(f"📈 Generating chart with {len(sparkline_data)} data points...")
    
    # Generate chart
    chart_data = chart_generator.create_sparkline_chart(
        data=sparkline_data,
        coin_name="bitcoin",
        price_change_24h=bitcoin['price_change_percentage_24h'],
        width=1080,
        height=600
    )
    
    if not chart_data:
        print("❌ Failed to generate chart")
        return False
    
    # Save chart
    chart_path = chart_generator.save_chart(
        chart_data=chart_data,
        filename="bitcoin_7day_chart",
        coin_name="bitcoin"
    )
    
    if chart_path:
        print(f"🎉 MVP Complete! Chart saved to: {chart_path}")
        return True
    else:
        print("❌ Failed to save chart")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)