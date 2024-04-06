from django.test import TestCase
from django.utils import timezone
from src.apps.market_trends.models import CurrencyData


class CurrencyDataModelTests(TestCase):
    def test_currency_data_str(self):
        """Testa se o método __str__ do modelo CurrencyData retorna a string esperada."""
        test_pair = "BRLBTC"
        test_timestamp = timezone.now()
        currency_data = CurrencyData(
            pair=test_pair,
            mms_20=0.0,
            mms_50=0.0,
            mms_200=0.0,
            timestamp=test_timestamp,
        )

        expected_object_name = (
            f"{test_pair} - {test_timestamp.strftime('%d/%m/%Y %H:%M:%S')}"
        )
        self.assertEqual(str(currency_data), expected_object_name)
