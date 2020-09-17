from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CoordinatesRequestViewSet


router = DefaultRouter()
router.register(r'coordinates-request', CoordinatesRequestViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
