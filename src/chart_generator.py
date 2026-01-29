import os
import requests
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class QuickChartGenerator:
    def __init__(self):
        self.base_url = os.getenv('QUICKCHART_BASE_URL', 'https://quickchart.io/chart')
        self.session = requests.Session()
        
    def create_sparkline_chart(self, data, coin_name, price_change_24h, width=800, height=400):
        """
        Create a sparkline chart for cryptocurrency data
        """
        # Determine color based on price change
        if price_change_24h >= 0:
            line_color = '#00ff88'  # Green for positive
            fill_color = 'rgba(0, 255, 136, 0.1)'
        else:
            line_color = '#ff4444'  # Red for negative
            fill_color = 'rgba(255, 68, 68, 0.1)'
        
        chart_config = {
            "type": "line",
            "data": {
                "labels": list(range(len(data))),
                "datasets": [{
                    "data": data,
                    "borderColor": line_color,
                    "backgroundColor": fill_color,
                    "borderWidth": 4,
                    "fill": True,
                    "tension": 0.4,
                    "pointRadius": 0,
                    "pointHoverRadius": 0
                }]
            },
            "options": {
                "responsive": True,
                "maintainAspectRatio": False,
                "plugins": {
                    "legend": {
                        "display": False
                    },
                    "tooltip": {
                        "enabled": False
                    }
                },
                "scales": {
                    "x": {
                        "display": False,
                        "grid": {
                            "display": False
                        }
                    },
                    "y": {
                        "display": False,
                        "grid": {
                            "display": False
                        }
                    }
                },
                "elements": {
                    "line": {
                        "borderCapStyle": 'round',
                        "borderJoinStyle": 'round'
                    }
                }
            }
        }
        
        params = {
            'c': json.dumps(chart_config),
            'w': width,
            'h': height,
            'format': 'png',
            'backgroundColor': 'transparent'
        }
        
        try:
            response = self.session.get(self.base_url, params=params)
            response.raise_for_status()
            return response.content
        except requests.exceptions.RequestException as e:
            print(f"Error generating chart: {e}")
            return None
    
    def save_chart(self, chart_data, filename, coin_name):
        """
        Save chart image to file
        """
        charts_dir = os.getenv('CHARTS_DIR', './assets/charts')
        os.makedirs(charts_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = os.path.join(charts_dir, f"{coin_name}_{timestamp}_{filename}.png")
        
        try:
            with open(filepath, 'wb') as f:
                f.write(chart_data)
            print(f"Chart saved: {filepath}")
            return filepath
        except Exception as e:
            print(f"Error saving chart: {e}")
            return None