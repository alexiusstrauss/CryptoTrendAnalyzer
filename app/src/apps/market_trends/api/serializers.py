from rest_framework import serializers
from src.apps.market_trends.models import CurrencyData
from src.apps.market_trends.services import RANGE_FIELD_MAPPING


class CurrencyDataSerializer(serializers.ModelSerializer):
    timestamp = serializers.SerializerMethodField()
    mms = serializers.SerializerMethodField()

    class Meta:
        model = CurrencyData
        fields = ["timestamp", "mms"]

    def get_timestamp(self, obj):
        return int(obj.timestamp.timestamp())

    def get_mms(self, obj):
        range_value = self.context["request"].query_params.get("range")

        if mms_field := RANGE_FIELD_MAPPING.get(str(range_value)):
            return getattr(obj, mms_field, None)

        return None
