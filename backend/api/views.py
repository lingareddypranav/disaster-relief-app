from django.shortcuts import render

# Create your views here.
# api/views.py
# backend/api/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .utils.resource_allocation import calculate_resource_needs
from rest_framework import viewsets
from .models import Hurricane, Resource, DistributionCenter, Vehicle
from .serializers import (
    HurricaneSerializer, ResourceSerializer,
    DistributionCenterSerializer, VehicleSerializer
)

@api_view(['GET'])
def resource_needs(request):
    needs = calculate_resource_needs()
    return Response(needs)

@api_view(['POST'])
def dispatch_resources(request):
    adjusted_needs = request.data
    vehicles = []
    for res_type, quantity in adjusted_needs.items():
        # Create a vehicle for each resource type
        route = [
            {'latitude': 25.7617, 'longitude': -80.1918},  # Start point (e.g., Miami)
            {'latitude': 29.9511, 'longitude': -90.0715}   # End point (e.g., New Orleans)
        ]
        vehicle = Vehicle.objects.create(
            type=res_type,
            current_location=f"{route[0]['latitude']}, {route[0]['longitude']}",
            destination=f"{route[-1]['latitude']}, {route[-1]['longitude']}",
            route=route,
            status='en route'
        )
        vehicles.append(vehicle)
    return Response({'status': 'Resources dispatched'})


class HurricaneViewSet(viewsets.ModelViewSet):
    queryset = Hurricane.objects.all()
    serializer_class = HurricaneSerializer

class ResourceViewSet(viewsets.ModelViewSet):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer

class DistributionCenterViewSet(viewsets.ModelViewSet):
    queryset = DistributionCenter.objects.all()
    serializer_class = DistributionCenterSerializer

class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
