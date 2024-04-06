import time
from datetime import datetime, timedelta

import pandas as pd
import pytz
from django.db.models.query import QuerySet
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from .models import CurrencyData

RANGE_FIELD_MAPPING = {
    "20": "mms_20",
    "50": "mms_50",
    "200": "mms_200",
}


class CurrencyDataService:
    @staticmethod
    def filter_data(pair: str, from_date: str, to_date: str, range_value: str) -> QuerySet:
        # Converte as strings para inteiros e depois para objetos datetime com fuso horário UTC
        try:
            from_date_dt = datetime.fromtimestamp(int(from_date), pytz.UTC)
            to_date_dt = datetime.fromtimestamp(int(to_date), pytz.UTC)
        except ValueError as e:
            raise ValidationError("Invalid timestamp format. Timestamps should be integers representing Unix timestamps.") from e

        # Verificação de data maior que 365 dias, utilizando o UTC
        min_allowed_date = datetime.now(pytz.UTC) - timedelta(days=365)
        if from_date_dt < min_allowed_date:
            raise ValidationError("From date cannot be more than 365 days in the past.")

        # Valida o valor do range
        if range_value not in RANGE_FIELD_MAPPING:
            raise ValidationError("Invalid range value. Allowed values are 20, 50, 200.")

        # Busca os dados filtrados
        return CurrencyData.objects.filter(
            pair=pair,
            timestamp__gte=from_date_dt,
            timestamp__lte=to_date_dt,
        )

    @staticmethod
    def get_unix_timestamps():
        end_datetime = datetime.combine(datetime.now().date(), datetime.min.time())
        start_datetime = end_datetime - timedelta(days=367)
        start_unix_timestamp = int(time.mktime(start_datetime.timetuple()))
        end_unix_timestamp = int(time.mktime(end_datetime.timetuple()))

        return start_unix_timestamp, end_unix_timestamp

    @staticmethod
    def check_days_without_records():
        today = timezone.now().date() - timezone.timedelta(days=0)
        start_date = today - timezone.timedelta(days=365)

        queryset = CurrencyData.objects.filter(timestamp__gte=start_date).values("timestamp")
        df = pd.DataFrame(list(queryset))

        df["date"] = pd.to_datetime(df["timestamp"].apply(timezone.make_aware)).dt.date

        hoje = timezone.now().date()
        todas_as_datas = pd.date_range(start=start_date, end=hoje, freq="D").date

        datas_presentes = df["date"].unique()
        return [data for data in todas_as_datas if data not in datas_presentes]
