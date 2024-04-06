import datetime

import pytz
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase
from src.apps.market_trends.models import CurrencyData


class CurrencyDataViewSetTests(APITestCase):
    reverse_url = "currencydata-mms-list"

    @classmethod
    def setUpTestData(cls):
        # Criando dados mockados para testes
        cls.currency_data_list = [
            CurrencyData.objects.create(
                pair="BRLBTC",
                mms_20=11972.823214576,
                mms_50=0,
                mms_200=0,
                timestamp=timezone.make_aware(datetime.datetime.fromtimestamp(1707879600), pytz.utc),
            ),
            CurrencyData.objects.create(
                pair="BRLBTC",
                mms_20=12119.999395726,
                mms_50=0,
                mms_200=0,
                timestamp=timezone.make_aware(
                    datetime.datetime.fromtimestamp(1707966000), pytz.utc
                ),
            ),
            CurrencyData.objects.create(
                pair="BRLBTC",
                mms_20=12260.6985607045,
                mms_50=0,
                mms_200=0,
                timestamp=timezone.make_aware(
                    datetime.datetime.fromtimestamp(1708052400), pytz.utc
                ),
            ),
        ]

    def test_list_missing_from_param(self):
        # sourcery skip: class-extract-method
        """
        Testa se a view retorna 400 Bad Request quando o parâmetro 'from' está ausente.
        """
        url = reverse(self.reverse_url, kwargs={"pair": "BRLBTC"})
        response = self.client.get(url, {"to": "1777836800", "range": "20"})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_missing_to_param(self):
        """
        Testa se a view retorna 400 Bad Request quando o parâmetro 'to' está ausente.
        """
        url = reverse(self.reverse_url, kwargs={"pair": "BRLBTC"})
        response = self.client.get(url, {"from": "1777836800", "range": "20"})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_missing_range_param(self):
        """
        Testa se a view retorna 400 Bad Request quando o parâmetro 'range' está ausente.
        """
        url = reverse(self.reverse_url, kwargs={"pair": "BRLBTC"})
        response = self.client.get(url, {"from": "1777836800", "to": "1609459200"})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_invalid_range_param(self):
        """
        Testa se a view retorna 400 Bad Request quando o parâmetro 'range' está fora dos valores permitidos.
        """
        url = reverse(self.reverse_url, kwargs={"pair": "BRLBTC"})
        payload = {
            "from": "1777836800",
            "to": "1609459200",
            "range": "15",  # Valor fora do Range permitido
        }
        response = self.client.get(url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_invalid_pair(self):
        """
        Testa se a view retorna 404 Bad Request quando o PAIR está fora dos pares permitidos.
        """
        url = "/market_trends/BRLADA/mms/"
        payload = {
            "from": "1777836800",
            "to": "1609459200",
            "range": "20",
        }
        response = self.client.get(url, payload)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_currency_schema_ok(self):
        """
        Testa se a CurrencyDataViewSet retorna apenas os dados com schema correto
        """
        url = reverse(self.reverse_url, kwargs={"pair": "BRLBTC"})
        payload = {"from": "1707879600", "to": "1608052400", "range": "20"}
        response = self.client.get(url, payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsInstance(response.json(), list)

        for item in response.json():
            self.assertTrue("timestamp" in item and "mms" in item)
            self.assertIsInstance(item["timestamp"], float)
            self.assertIsInstance(item["mms"], float)

    def test_params_error_400(self):
        """
        Testa se a view retorna 400 os parâmetros não são fornecidos
        """
        url = reverse(self.reverse_url, kwargs={"pair": "BRLBTC"})
        payload = {}

        response = self.client.get(url, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
