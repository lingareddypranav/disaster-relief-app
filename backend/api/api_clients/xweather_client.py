# backend/api/api_clients/xweather_client.py
import requests
from django.conf import settings

class XWeatherClient:
    BASE_URL = 'https://data.api.xweather.com/tropicalcyclones/'

    def __init__(self):
        self.client_id = settings.XWEATHER_CLIENT_ID
        self.client_secret = settings.XWEATHER_CLIENT_SECRET

    def get_current_storms(self):
        params = {
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }
        try:
            response = requests.get(self.BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()
            print("xWeather API Response Data:", data)

            if data.get('success'):
                storms = data.get('response', [])
                if not storms:
                    print("No storms data retrieved from xWeather API.")
                return storms
            else:
                error_message = data.get('error', 'Unknown error occurred.')
                print(f"API Error: {error_message}")
                return []
        except requests.RequestException as e:
            print(f"Exception occurred: {e}")
            return []
