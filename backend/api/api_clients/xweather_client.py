import requests
from django.conf import settings

class XWeatherClient:
    BASE_URL = 'https://data.api.xweather.com/tropicalcyclones/within'

    def __init__(self):
        self.client_id = settings.XWEATHER_CLIENT_ID
        self.client_secret = settings.XWEATHER_CLIENT_SECRET

    def get_current_storms(self, bbox):
        p = f"{bbox['north_lat']},{bbox['west_lon']},{bbox['south_lat']},{bbox['east_lon']}"
        params = {
            'p': p,
            'filter': 'all',
            'limit': 10,
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }
        try:
            response = requests.get(self.BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()
            if data.get('success'):
                return data['results']
            else:
                error_description = data.get('error', {}).get('description', 'Unknown error')
                print(f"An error occurred: {error_description}")
                return []  # Make sure it returns a list, even if empty
        except requests.RequestException as e:
            print(f"Exception occurred: {e}")
            return []  # Again, ensure it returns a list
