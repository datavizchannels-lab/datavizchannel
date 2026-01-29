import os
import requests
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class CoingeckoAPI:
    def __init__(self):
        self.base_url = os.getenv('COINGECKO_BASE_URL', 'https://api.coingecko.com/api/v3')
        self.session = requests.Session()
        
    def get_coin_markets(self, vs_currency='usd', order='market_cap_desc', 
                         per_page=10, page=1, sparkline=True):
        """
        Get top cryptocurrencies by market cap with sparkline data
        """
        endpoint = f"{self.base_url}/coins/markets"
        params = {
            'vs_currency': vs_currency,
            'order': order,
            'per_page': per_page,
            'page': page,
            'sparkline': sparkline,
            'price_change_percentage': '24h'
        }
        
        try:
            response = self.session.get(endpoint, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching coin markets: {e}")
            return None
    
    def get_simple_price(self, coin_ids, vs_currencies='usd', include_market_cap='false',
                        include_24hr_vol='false', include_24hr_change='false', 
                        include_last_updated_at='false'):
        """
        Get current price for specific coins
        """
        endpoint = f"{self.base_url}/simple/price"
        params = {
            'ids': ','.join(coin_ids) if isinstance(coin_ids, list) else coin_ids,
            'vs_currencies': vs_currencies,
            'include_market_cap': include_market_cap,
            'include_24hr_vol': include_24hr_vol,
            'include_24hr_change': include_24hr_change,
            'include_last_updated_at': include_last_updated_at
        }
        
        try:
            response = self.session.get(endpoint, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching simple price: {e}")
            return None
    
    def get_top_gainers(self, limit=5):
        """
        Get top gainers in the last 24 hours
        """
        markets = self.get_coin_markets(per_page=50, sparkline=True)
        if not markets:
            return None
            
        # Filter by positive price change and sort
        gainers = [coin for coin in markets if coin.get('price_change_percentage_24h', 0) > 0]
        gainers.sort(key=lambda x: x.get('price_change_percentage_24h', 0), reverse=True)
        
        return gainers[:limit]
    
    def get_top_losers(self, limit=5):
        """
        Get top losers in the last 24 hours
        """
        markets = self.get_coin_markets(per_page=50, sparkline=True)
        if not markets:
            return None
            
        # Filter by negative price change and sort
        losers = [coin for coin in markets if coin.get('price_change_percentage_24h', 0) < 0]
        losers.sort(key=lambda x: x.get('price_change_percentage_24h', 0))
        
        return losers[:limit]
    
    def get_coin_price_history(self, coin_id, vs_currency='usd', days=7):
        """
        Get historical price data for a specific coin
        """
        endpoint = f"{self.base_url}/coins/{coin_id}/market_chart"
        params = {
            'vs_currency': vs_currency,
            'days': days,
            'interval': 'daily'
        }
        
        try:
            response = self.session.get(endpoint, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Extract just the prices
            prices = [price[1] for price in data['prices']]
            return prices
        except requests.exceptions.RequestException as e:
            print(f"Error fetching price history: {e}")
            return None