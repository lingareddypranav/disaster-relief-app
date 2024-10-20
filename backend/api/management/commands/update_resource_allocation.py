from django.core.management.base import BaseCommand
from api.api_clients.gemini_ai_client import GeminiAIClient
from api.models import Hurricane, Vehicle, DistributionCenter
from api.utils.census_data import get_county_population
import json
import requests
import re

class Command(BaseCommand):
    help = 'Updates resource allocation data using the Gemini AI API'

    def handle(self, *args, **options):
    # Fetch the latest hurricane data
        try:
            hurricane = Hurricane.objects.latest('timestamp')
        except Hurricane.DoesNotExist:
            self.stdout.write(self.style.WARNING('No hurricane data available.'))
            return

        # Since we're skipping affected counties, let's assume a fixed population
        population = self.get_total_population()

        # Prepare the prompt for the Gemini API
        prompt = self.construct_prompt(hurricane, population)

        # Initialize Gemini AI client
        gemini_client = GeminiAIClient()

        # Generate resource allocation
        response_text = gemini_client.generate_resource_allocation(prompt)

        # Print the AI response for debugging
        print("Gemini AI API Response:")
        print(response_text)

        # Parse the response and update the database
        success = self.process_response(response_text)

        if success:
            self.stdout.write(self.style.SUCCESS('Successfully updated resource allocation data.'))
        else:
            self.stdout.write(self.style.ERROR('Failed to update resource allocation data.'))


    def get_total_population(self):
        """
        Returns the total population to be used in resource allocation.
        """
        # For simplicity, we'll use a fixed population number
        # Alternatively, fetch the state population using PopulationClient
        return 21538187  # Approximate population of Florida as of 2020 census

    def construct_prompt(self, hurricane, population):
        prompt = f"""
                You are an AI assistant tasked with allocating resources for disaster relief.

                Hurricane Details:
                - Name: {hurricane.name}
                - Category: {hurricane.category}
                - Current Location: {hurricane.current_location}

                Affected Population:
                - Total Population: {population}

                Based on the above information, determine the required quantities of the following resources:
                - Food (in tons)
                - Water (in liters)
                - Medical Supplies (in units)

                **Important Instructions:**
                - Your response **must** be in **valid JSON format**.
                - **Do not include any explanations, notes, or additional text.**
                - **Output only the JSON object.**

                Provide a JSON response in the following format:

                {{
                    "resource_allocation": [
                    {{
                        "type": "food",
                        "quantity": 100,
                        "distribution_center": "DC1",
                        "route": [
                            {{"latitude": 28.5383, "longitude": -81.3792}},
                            {{"latitude": 27.9506, "longitude": -82.4572}}
                        ]
                     }},
                    {{
                        "type": "water",
                        "quantity": 200,
                        "distribution_center": "DC2",
                        "route": [
                            {{"latitude": 28.5383, "longitude": -81.3792}},
                            {{"latitude": 25.7617, "longitude": -80.1918}}
                        ]
                    }},
                    {{
                    "type": "medical",
                    "quantity": 50,
                    "distribution_center": "DC3",
                    "route": [
                            {{"latitude": 28.5383, "longitude": -81.3792}},
                            {{"latitude": 26.1224, "longitude": -80.1373}}
                            ]
                     }}
                    ]
                }}

                **Remember: Only output the JSON object and nothing else.**
                """
        return prompt


    def process_response(self, response_text):
        """
        Parses the response from the Gemini API and updates the database.
        """
        # Attempt to extract JSON from the response using regex
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            json_str = json_match.group(0)
            try:
                response_data = json.loads(json_str)
            except json.JSONDecodeError:
                self.stdout.write(self.style.ERROR('Failed to parse JSON from extracted response.'))
                return False  # Return False to indicate failure
        else:
            self.stdout.write(self.style.ERROR('No JSON object found in the response.'))
            return False  # Return False to indicate failure

        resource_allocations = response_data.get('resource_allocation', [])
        if not resource_allocations:
            self.stdout.write(self.style.WARNING('No resource allocations found in the response.'))
            return False  # Return False to indicate failure

        # Clear existing vehicles and distribution centers
        Vehicle.objects.all().delete()
        DistributionCenter.objects.all().delete()

        for allocation in resource_allocations:
        # Create or get the distribution center
            dc_name = allocation.get('distribution_center', 'Unknown DC')
            dc, created = DistributionCenter.objects.get_or_create(
                name=dc_name,
                defaults={'location': 'Unknown', 'latitude': None, 'longitude': None}
            )

            # Generate a sample route from the distribution center to the affected area
            # For simplicity, we'll use fixed coordinates for the distribution center and destination
            sample_route = [
                {"latitude": 28.5383, "longitude": -81.3792},  # Orlando, FL (distribution center)
                {"latitude": 25.7617, "longitude": -80.1918}   # Miami, FL (affected area)
            ]

            # Update the allocation's route if it's empty
            if not allocation.get('route'):
                allocation['route'] = sample_route

            # Create the vehicle
            vehicle_type = allocation.get('type', 'unknown')
            quantity = allocation.get('quantity', 0)
            route = allocation.get('route', [])
            vehicle = Vehicle.objects.create(
                type=vehicle_type,
                current_location=dc.location,
                destination='Affected Area',
                route=route,
                status='en route',
                quantity=quantity
            )
            self.stdout.write(self.style.SUCCESS(f"Created vehicle: {vehicle} carrying {quantity} units of {vehicle_type}"))

        return True  # Return True to indicate success