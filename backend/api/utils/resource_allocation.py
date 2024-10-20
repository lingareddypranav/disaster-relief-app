# api/utils/resource_allocation.py
from api.models import Hurricane
from ..api_clients.population_client import PopulationClient
from django.core.exceptions import ObjectDoesNotExist

def calculate_resource_needs():
    # Get the latest hurricane
    try:
        hurricane = Hurricane.objects.latest('timestamp')
    except ObjectDoesNotExist:
        print("No hurricanes found in the database.")
        return {'food': 0, 'water': 0, 'medical': 0}

    # Use forecasted_path to determine affected counties
    affected_counties = get_affected_counties(hurricane.forecasted_path)

    # Initialize population client
    population_client = PopulationClient()

    total_resources = {'food': 0, 'water': 0, 'medical': 0}

    for county in affected_counties:
        state_fips = county['state_fips']
        county_fips = county['county_fips']
        population_data = population_client.get_population_by_county(state_fips, county_fips)
        if len(population_data) > 1:
            population = int(population_data[1][0])
            # Resource calculation logic
            food_needed = population * 2  # 2 meals per person
            water_needed = population * 3  # 3 liters per person
            medical_needed = int(population * 0.05)  # 5% may need medical assistance

            total_resources['food'] += food_needed
            total_resources['water'] += water_needed
            total_resources['medical'] += medical_needed
        else:
            print(f"Failed to get population data for county {county_fips}, state {state_fips}")

    return total_resources

def get_affected_counties(forecasted_path):
    # Implement logic to determine affected counties based on forecasted_path
    # For now, simulate affected counties
    return [
        {'state_fips': '12', 'county_fips': '086'},  # Miami-Dade County, FL
        {'state_fips': '12', 'county_fips': '099'},  # Palm Beach County, FL
        # Add more counties as needed
    ]
