from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.response import Response
from src.apps.market_trends.api.swagger_schemas import CURRENCY_DATA_SCHEMA
from src.apps.market_trends.models import CurrencyData
from src.apps.market_trends.services import CurrencyDataService

from .serializers import CurrencyDataSerializer


class CurrencyDataViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CurrencyData.objects.all()
    serializer_class = CurrencyDataSerializer

    def get_params(self):
        pair = self.kwargs.get("pair")
        from_date = self.request.query_params.get("from")
        to_date = self.request.query_params.get("to")
        range_value = self.request.query_params.get("range")

        if not all([from_date, to_date, range_value]):
            return None, {"error": "All parameters (from, to, range) are required."}

        return (pair, from_date, to_date, range_value), None

    def get_queryset(self):
        params, _ = self.get_params()
        if params:
            pair, from_date, to_date, range_value = params
            return CurrencyDataService.filter_data(pair, from_date, to_date, range_value)

    @swagger_auto_schema(**CURRENCY_DATA_SCHEMA)
    def list(self, request, *args, **kwargs):
        _, error = self.get_params()
        if error:
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

        return super().list(request, *args, **kwargs)
