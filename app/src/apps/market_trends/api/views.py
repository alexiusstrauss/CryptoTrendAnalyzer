from rest_framework import status, viewsets
from rest_framework.response import Response
from src.apps.market_trends.models import CurrencyData

from .serializers import CurrencyDataSerializer


class CurrencyDataViewSet(viewsets.ModelViewSet):
    queryset = CurrencyData.objects.all()
    serializer_class = CurrencyDataSerializer

    def list(self, request, *args, **kwargs):
        pair = request.query_params.get("pair")
        from_date = request.query_params.get("from")
        to_date = request.query_params.get("to")
        range_value = request.query_params.get("range")

        if not all([pair, from_date, to_date, range_value]):
            return Response(
                {"error": "All parameters (pair, from, to, range) are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().list(request, *args, **kwargs)
