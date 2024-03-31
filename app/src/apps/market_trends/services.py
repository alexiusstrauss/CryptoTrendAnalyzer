import time
from datetime import datetime, timedelta

import pandas as pd
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
    def filter_data(pair: str, from_date_str: str, to_date_str: str, range_value: str) -> QuerySet:
        try:
            from_date = datetime.strptime(from_date_str, "%Y-%m-%d")
            to_date = datetime.strptime(to_date_str, "%Y-%m-%d")
        except ValueError as e:
            raise ValidationError("Invalid date format. Please use YYYY-MM-DD.") from e

        min_allowed_date = datetime.now() - timedelta(days=365)
        if from_date < min_allowed_date:
            raise ValidationError("From date cannot be more than 365 days in the past.")

        if field_name := RANGE_FIELD_MAPPING.get(range_value):
            return CurrencyData.objects.filter(
                pair=pair,
                timestamp__gte=from_date,
                timestamp__lte=to_date,
            ).values("pair", field_name, "timestamp")

        raise ValidationError("Invalid range value. Allowed values are 20, 50, 200.")

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
