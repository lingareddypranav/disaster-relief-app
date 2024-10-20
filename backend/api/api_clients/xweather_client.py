# backend/api/api_clients/xweather_client.py

import requests
from django.conf import settings

class XWeatherClient:
    BASE_URL = 'https://data.api.xweather.com/tropicalcyclones/archive/'

    def __init__(self):
        self.client_id = settings.XWEATHER_CLIENT_ID
        self.client_secret = settings.XWEATHER_CLIENT_SECRET
    
    def get_hurricane_milton(self):
        params = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
        }
        endpoint = f"{self.BASE_URL}2024-AL-14?"  # Specific endpoint for Hurricane Milton
        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            data = response.json()
            print("xWeather Archive API Response Data:", data)
            if data.get('success'):
                storm = data.get('response', {})
                if not storm:
                    print("No data retrieved for Hurricane Milton from xWeather API.")
                return storm
            else:
                error_message = data.get('error', 'Unknown error occurred.')
                print(f"API Error: {error_message}")
                return {}
        except requests.HTTPError as e:
            print(f"HTTPError occurred: {e}")
            print(f"Response status code: {response.status_code}")
            print(f"Response content: {response.content.decode()}")
            return {}
        except requests.RequestException as e:
            print(f"Exception occurred: {e}")
            return {}

    #  def get_historical_storms(self, location='Miami,FL', radius_miles=300, start_date='-5years', limit=1):
    #     params = {
    #         'client_id': self.client_id,
    #         'client_secret': self.client_secret,
    #         'p': location,
    #         'radius': f'{radius_miles}miles',
    #         'from': start_date,
    #         'to': 'now',
    #         'limit': limit,
    #         'sort': 'id:-1',
    #         'fields': 'id,profile,position,track,forecast'
    #     }
    #     endpoint = self.BASE_URL
    #     try:
    #         response = requests.get(endpoint, params=params)
    #         response.raise_for_status()
    #         data = response.json()
    #         print("xWeather Archive API Response Data:", data)
    #         if data.get('success'):
    #             storms = data.get('response', [])
    #             if not storms:
    #                 print("No historical storms data retrieved from xWeather API.")
    #             return storms
    #         else:
    #             error_message = data.get('error', 'Unknown error occurred.')
    #             print(f"API Error: {error_message}")
    #             return []
    #     except requests.HTTPError as e:
    #         print(f"HTTPError occurred: {e}")
    #         print(f"Response status code: {response.status_code}")
    #         print(f"Response content: {response.content.decode()}")
    #         return []
    #     except requests.RequestException as e:
    #         print(f"Exception occurred: {e}")
    #         return [] 
