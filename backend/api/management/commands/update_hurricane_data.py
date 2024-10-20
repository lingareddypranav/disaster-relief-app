# backend/api/management/commands/update_hurricane_data.py
from django.core.management.base import BaseCommand
from api.api_clients.xweather_client import XWeatherClient
from api.models import Hurricane
import datetime

class Command(BaseCommand):
    help = 'Updates hurricane data from xWeather API'

    def handle(self, *args, **options):
        client = XWeatherClient()
        storms = client.get_current_storms()

        if not storms:
            self.stdout.write(self.style.WARNING('No storms data retrieved from xWeather API.'))
            return

        self.stdout.write(self.style.SUCCESS(f"Retrieved {len(storms)} storms from xWeather API."))

        for storm in storms:
            # Extract necessary data from the storm object
            name = storm.get('profile', {}).get('name', 'Unknown')
            category_code = storm.get('profile', {}).get('maxStormCat', 'TD')
            category = self.get_category_number(category_code)

            # Extract current location
            position = storm.get('position', {})
            loc = position.get('loc', {})
            if loc:
                current_location = f"{loc.get('lat', 0)}, {loc.get('long', 0)}"
            else:
                current_location = '0, 0'  # Default if no position data

            # Get forecasted path
            forecast = storm.get('forecast', [])
            forecasted_path = []
            for point in forecast:
                point_loc = point.get('loc', {})
                if point_loc:
                    forecasted_path.append({
                        'latitude': point_loc.get('lat', 0),
                        'longitude': point_loc.get('long', 0)
                    })

            # Get past track
            track = storm.get('track', [])
            past_path = []
            for point in track:
                point_loc = point.get('loc', {})
                if point_loc:
                    past_path.append({
                        'latitude': point_loc.get('lat', 0),
                        'longitude': point_loc.get('long', 0)
                    })

            # Print the extracted data for debugging
            self.stdout.write(f"Processing storm: {name}")
            self.stdout.write(f"Category Code: {category_code} (Category {category})")
            self.stdout.write(f"Current Location: {current_location}")
            self.stdout.write(f"Forecasted Path Points: {len(forecasted_path)}")
            self.stdout.write(f"Past Path Points: {len(past_path)}")

            # Save or update hurricane data
            Hurricane.objects.update_or_create(
                name=name,
                defaults={
                    'category': category,
                    'current_location': current_location,
                    'forecasted_path': forecasted_path,
                    'past_path': past_path,
                    'timestamp': datetime.datetime.now(),
                }
            )

        self.stdout.write(self.style.SUCCESS('Successfully updated hurricane data'))

    def get_category_number(self, category_code):
        # Map category codes to numbers
        category_mapping = {
            'TD': 0,  # Tropical Depression
            'TS': 1,  # Tropical Storm
            'H1': 1,  # Category 1 Hurricane
            'H2': 2,  # Category 2 Hurricane
            'H3': 3,  # Category 3 Hurricane
            'H4': 4,  # Category 4 Hurricane
            'H5': 5,  # Category 5 Hurricane
            # Add more mappings if necessary
        }
        return category_mapping.get(category_code, 0)
