# api/utils/census_data.py

import requests
from django.conf import settings  # Import settings to access CENSUS_API_KEY

def get_county_population(county_fips_codes):
    """
    Fetches the population data for the given county FIPS codes.
    """
    api_key = settings.CENSUS_API_KEY  # Use the Census API key from settings
    base_url = 'https://api.census.gov/data/2020/dec/pl'
    populations = {}

    for fips_code in county_fips_codes:
        state_fips = fips_code[:2]
        county_fips = fips_code[2:]
        params = {
            'get': 'P1_001N',  # Total population
            'for': f'county:{county_fips}',
            'in': f'state:{state_fips}',
            'key': api_key,
        }
        response = requests.get(base_url, params=params)
        data = response.json()
        if len(data) > 1:
            populations[fips_code] = int(data[1][0])
        else:
            populations[fips_code] = 0  # Default to 0 if no data

    return populations
