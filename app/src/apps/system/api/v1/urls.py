from django.urls import path
from rest_framework import routers

from .views import HealthCheckView

router = routers.DefaultRouter()

urlpatterns = [
    path("healthcheck", HealthCheckView.as_view(), name='health_check'),
]
