from django.core.management.base import BaseCommand
from api.api_clients.xweather_client import XWeatherClient
from api.models import Hurricane
import datetime

class Command(BaseCommand):
    help = 'Updates hurricane data from xWeather API'

    def handle(self, *args, **options):
        client = XWeatherClient()
        # Adjust the bbox to cover areas where hurricanes occur
        bbox = {
            'north_lat': 50.0,   # Northern latitude
            'west_lon': -100.0,  # Western longitude
            'south_lat': 5.0,    # Southern latitude
            'east_lon': -10.0    # Eastern longitude
        }
        storms = client.get_current_storms(bbox)

        if not isinstance(storms, list):
            print("Unexpected response format for storms data.")
            return

        for storm in storms:
            if isinstance(storm, dict) and 'profile' in storm:
                Hurricane.objects.update_or_create(
                    name=storm['profile']['name'],
                    defaults={
                        'category': storm.get('category', 1),
                        'current_location': f"{storm['location']['latitude']}, {storm['location']['longitude']}",
                        'forecasted_path': storm.get('forecasted_path', []),
                        'past_path': storm.get('past_path', []),
                        'timestamp': datetime.datetime.now(),
                    }
                )
            else:
                print(f"Unexpected format for storm data: {storm}")

        self.stdout.write(self.style.SUCCESS('Successfully updated hurricane data'))
