from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase


class HealthCheckTests(APITestCase):
    def test_health_check_status(self):
        """
        Garante que o endpoint de health check esteja funcionando e retorne status 200.
        """
        client = APIClient()
        response = client.get(reverse("health_check"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"status": "UP", "message": "API is running smoothly."})
