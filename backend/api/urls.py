# backend/api/urls.py
from django.urls import path, include
from rest_framework import routers
from .views import (
    HurricaneViewSet, ResourceViewSet,
    DistributionCenterViewSet, VehicleViewSet, resource_needs, dispatch_resources,
)

router = routers.DefaultRouter()
router.register(r'hurricanes', HurricaneViewSet)
router.register(r'resources', ResourceViewSet)
router.register(r'distribution-centers', DistributionCenterViewSet)
router.register(r'vehicles', VehicleViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('resource-needs/', resource_needs, name='resource-needs'),
    path('dispatch-resources/', dispatch_resources, name='dispatch-resources'),
]
