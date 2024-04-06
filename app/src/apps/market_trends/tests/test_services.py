import datetime
import time
from datetime import datetime, timedelta

from django.test import TestCase
from rest_framework.exceptions import ValidationError
from src.apps.market_trends.services import CurrencyDataService


class CurrencyDataServiceTests(TestCase):

    def test_get_unix_timestamps(self):
        """
        Testa se o método get_unix_timestamps retorna os timestamps Unix corretos
        para o início e fim com base na lógica definida.
        """
        # Executa o método que está sendo testado
        start_unix_timestamp, end_unix_timestamp = (
            CurrencyDataService.get_unix_timestamps()
        )

        # Calcula os timestamps esperados para comparação
        end_expected_datetime = datetime.combine(
            datetime.now().date(), datetime.min.time()
        )
        start_expected_datetime = end_expected_datetime - timedelta(days=367)
        start_expected_unix_timestamp = int(
            time.mktime(start_expected_datetime.timetuple())
        )
        end_expected_unix_timestamp = int(
            time.mktime(end_expected_datetime.timetuple())
        )

        # Compara os resultados
        self.assertEqual(start_unix_timestamp, start_expected_unix_timestamp)
        self.assertEqual(end_unix_timestamp, end_expected_unix_timestamp)

    def test_filter_data_with_invalid_timestamp_format(self):
        """
        Testa se um ValidationError é levantado quando os timestamps fornecidos
        possuem um formato inválido.
        """
        with self.assertRaises(ValidationError) as context:
            CurrencyDataService.filter_data(
                "BRLBTC", "invalid_timestamp", "1609459200", "20"
            )

        self.assertIn("Invalid timestamp format", str(context.exception))

    def test_filter_data_with_too_old_date(self):
        """
        Testa se um ValidationError é levantado quando a data 'from' é mais antiga
        do que o permitido (mais de 365 dias no passado).
        """
        too_old_date = (datetime.now() - timedelta(days=366)).timestamp()
        with self.assertRaises(ValidationError) as context:
            CurrencyDataService.filter_data(
                "BRLBTC", str(int(too_old_date)), str(int(time.time())), "20"
            )

        self.assertIn(
            "From date cannot be more than 365 days in the past", str(context.exception)
        )
