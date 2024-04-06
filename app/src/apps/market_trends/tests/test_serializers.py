from unittest.mock import Mock

import pytest
from django.utils import timezone
from src.apps.market_trends.api.serializers import CurrencyDataSerializer
from src.apps.market_trends.models import CurrencyData

TEST_RANGE_FIELD_MAPPING = {
    "20": "mms_20",
    "50": "mms_50",
    "200": "mms_200",
}


@pytest.fixture
def currency_data_instance():
    """Cria uma instância mock do modelo CurrencyData para uso nos testes."""
    return CurrencyData(pair="BRLBTC", mms_20=0.2, mms_50=0.5, mms_200=2.0, timestamp=timezone.now())


@pytest.mark.django_db
def test_currency_data_serializer_timestamp(currency_data_instance):
    """Testa se o campo 'timestamp' do serializer retorna o valor esperado."""
    context = {"request": Mock()}
    serializer = CurrencyDataSerializer(instance=currency_data_instance, context=context)
    expected_timestamp = int(currency_data_instance.timestamp.timestamp())

    assert serializer.data["timestamp"] == expected_timestamp


@pytest.mark.django_db
def test_currency_data_serializer_mms(currency_data_instance):
    """Testa se o campo 'mms' do serializer retorna o valor correto baseado no 'range'."""

    # Teste para 'range' = '20'
    request_mock_20 = Mock(query_params={"range": "20"})
    context_20 = {"request": request_mock_20}
    serializer_20 = CurrencyDataSerializer(instance=currency_data_instance, context=context_20)
    expected_mms_20 = getattr(currency_data_instance, TEST_RANGE_FIELD_MAPPING["20"])
    assert serializer_20.data["mms"] == expected_mms_20, "Failed for range: 20"

    # Teste para 'range' = '50'
    request_mock_50 = Mock(query_params={"range": "50"})
    context_50 = {"request": request_mock_50}
    serializer_50 = CurrencyDataSerializer(instance=currency_data_instance, context=context_50)
    expected_mms_50 = getattr(currency_data_instance, TEST_RANGE_FIELD_MAPPING["50"])
    assert serializer_50.data["mms"] == expected_mms_50, "Failed for range: 50"

    # Teste para 'range' = '200'
    request_mock_200 = Mock(query_params={"range": "200"})
    context_200 = {"request": request_mock_200}
    serializer_200 = CurrencyDataSerializer(instance=currency_data_instance, context=context_200)
    expected_mms_200 = getattr(currency_data_instance, TEST_RANGE_FIELD_MAPPING["200"])
    assert serializer_200.data["mms"] == expected_mms_200, "Failed for range: 200"
