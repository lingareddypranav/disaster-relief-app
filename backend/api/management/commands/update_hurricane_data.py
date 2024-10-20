# backend/api/management/commands/update_hurricane_data.py

from django.core.management.base import BaseCommand
from api.api_clients.xweather_client import XWeatherClient
from api.models import Hurricane
import datetime

class Command(BaseCommand):
    help = 'Updates hurricane data from xWeather API (historical data)'

    def handle(self, *args, **options):
        # Clear existing hurricane data
        Hurricane.objects.all().delete()

        client = XWeatherClient()

        # Get past hurricane data
        storms = client.get_hurricane_milton()  # Fetch data for a specific past hurricane

        if not storms or len(storms) == 0:
            self.stdout.write(self.style.WARNING('No data retrieved for the specified hurricane from xWeather API.'))
            return

        # Get the first hurricane in the list
        storm = storms[0]

        # Extract necessary data from the API response
        name = storm.get('profile', {}).get('name', 'Unknown')
        category_code = storm.get('profile', {}).get('maxStormCat', 'TD')
        category = self.get_category_number(category_code)

        # Safely extract current location from historical data (if available)
        position = storm.get('position')
        if position and position.get('loc'):
            loc = position['loc']
            current_location = f"{loc.get('lat', 0)}, {loc.get('long', 0)}"
        else:
            current_location = '0, 0'  # Default if no position data

        # Get past track data (historical path of the hurricane)
        track = storm.get('track', [])  # Default to empty list if no track data
        past_path = []
        for point in track:
            point_loc = point.get('loc', {})
            if point_loc:
                    past_path.append({
                        'latitude': point_loc.get('lat', 0),
                        'longitude': point_loc.get('long', 0)
                })

        # Handle forecast data, which might be None for past hurricanes
        forecast = storm.get('forecast') or []  # Past hurricanes may have no forecast data
        forecasted_path = []
        for point in forecast:
            point_loc = point.get('loc', {})
            if point_loc:
                forecasted_path.append({
                    'latitude': point_loc.get('lat', 0),
                    'longitude': point_loc.get('long', 0)
                })

        # Save the hurricane data to the database
        Hurricane.objects.update_or_create(
            name=name,
            defaults={
                'category': category,
                'current_location': current_location,  # Historical location (not "current")
                'forecasted_path': forecasted_path,
                'past_path': past_path,
                'timestamp': datetime.datetime.now(),  # Timestamp for when data was updated
            }
        )

        self.stdout.write(self.style.SUCCESS(f'Successfully updated data for hurricane: {name}'))

    def get_category_number(self, category_code):
        # Map category codes to numbers
        category_mapping = {
            'TD': 0,  # Tropical Depression
            'TS': 1,  # Tropical Storm
            'H1': 1,  # Category 1 Hurricane
            'H2': 2,
            'H3': 3,
            'H4': 4,
            'H5': 5,
        }
        return category_mapping.get(category_code, 0)
