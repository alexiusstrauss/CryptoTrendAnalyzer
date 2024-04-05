from rest_framework import serializers
from src.apps.market_trends.models import CurrencyData


class CurrencyDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrencyData
        fields = ['pair', 'mms_20', 'mms_50', 'mms_200', 'timestamp']
