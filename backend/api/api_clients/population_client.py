# api/api_clients/population_client.py
# backend/api/api_clients/population_client.py
import requests
from django.conf import settings

class PopulationClient:
    BASE_URL = 'https://api.census.gov/data/2020/dec/pl'

    def get_population_by_county(self, state_fips, county_fips):
        params = {
            'get': 'P1_001N',
            'for': f'county:{county_fips}',
            'in': f'state:{state_fips}',
            'key': settings.CENSUS_API_KEY
        }
        try:
            response = requests.get(self.BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()
            return data
        except requests.RequestException as e:
            print(f"Error fetching population data: {e}")
            return []

