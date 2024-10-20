# api/serializers.py
from rest_framework import serializers
from .models import Hurricane, Resource, DistributionCenter, Vehicle

class HurricaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hurricane
        fields = '__all__'

class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = '__all__'

class DistributionCenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = DistributionCenter
        fields = '__all__'

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'
