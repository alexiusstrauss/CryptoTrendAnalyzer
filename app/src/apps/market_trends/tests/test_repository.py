from django.test import TestCase
from django.utils import timezone
from src.apps.market_trends.models import CurrencyData, ExecutionLog


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

        expected_object_name = f"{test_pair} - {test_timestamp.strftime('%d/%m/%Y %H:%M:%S')}"
        self.assertEqual(str(currency_data), expected_object_name)


class ExecutionLogModelTest(TestCase):

    def test_str_representation(self):
        """Testa a representação em string do modelo ExecutionLog."""
        time_now = timezone.now()
        log = ExecutionLog(status=200, log="Teste de execução bem-sucedida", created_at=time_now)
        expected_str = f"ExecutionLog {time_now} - Status 200"

        self.assertEqual(str(log), expected_str)
