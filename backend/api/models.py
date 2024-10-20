from django.db import models

class Hurricane(models.Model):
    name = models.CharField(max_length=100)
    category = models.IntegerField()
    current_location = models.CharField(max_length=100)
    forecasted_path = models.JSONField()
    past_path = models.JSONField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} (Category {self.category})"

class Resource(models.Model):
    RESOURCE_TYPES = [
        ('food', 'Food'),
        ('water', 'Water'),
        ('medical', 'Medical Supplies'),
    ]
    type = models.CharField(max_length=20, choices=RESOURCE_TYPES)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.type} - {self.quantity}"

class DistributionCenter(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    latitude = models.FloatField(null=True, blank=True)  # Add latitude
    longitude = models.FloatField(null=True, blank=True)  # Add longitude
    sustainability_notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Vehicle(models.Model):
    VEHICLE_TYPES = [
        ('food', 'Food Transport'),
        ('water', 'Water Transport'),
        ('medical', 'Medical Transport'),
        ('plane', 'Plane'),
    ]
    type = models.CharField(max_length=20, choices=VEHICLE_TYPES)
    current_location = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    route = models.JSONField()
    status = models.CharField(max_length=50)
    quantity = models.IntegerField(default=0)  # Added quantity field

    def __str__(self):
        return f"{self.type} - {self.status}"
