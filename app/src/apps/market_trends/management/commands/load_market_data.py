import pandas as pd
import requests
from django.core.management.base import BaseCommand
from django.utils import timezone
from requests.exceptions import RequestException
from src.apps.market_trends.models import CurrencyData
from src.apps.market_trends.services import CurrencyDataService


class Command(BaseCommand):
    help = "Carrega dados históricos de criptomoedas e calcula médias móveis simples MMS"

    def handle(self, *args, **kwargs):
        pairs = ["BRLBTC", "BRLETH"]
        self.stdout.write(self.style.WARNING(f"Carregando dados históricos para gerar MMS dos pares: {pairs}. "))
        for pair in pairs:
            try:
                self.stdout.write(self.style.WARNING(f"Processando dados do MMS de: {pair}."))
                self.process_pair(pair)
                self.stdout.write(self.style.SUCCESS(f"Dados de MMS do {pair} carregadas com sucesso."))
            except RequestException as e:
                self.stdout.write(self.style.ERROR(f"Erro ao processar dados para o pair: {pair}: {e}"))

        if days_without_record := CurrencyDataService.check_days_without_records():
            self.stdout.write(
                self.style.ERROR(f"Dias que não tem registros nos útimos 365 dias: {days_without_record}")
            )

    def process_pair(self, pair):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }

        initial_unix_date, final_unix_date = CurrencyDataService.get_unix_timestamps()

        url = f"https://mobile.mercadobitcoin.com.br/v4/{pair}/candle?from={initial_unix_date}&to={final_unix_date}&precision=1d"
        response = requests.get(url, headers=headers, timeout=5)

        if response.status_code == 200:
            data = response.json()
            candles = data.get("candles", [])
            df = self.prepare_dataframe(candles)
            self.populate_database(pair, df)
        else:
            self.stdout.write(self.style.WARNING(f"Não foi possível obter dados para {pair}."))

    def prepare_dataframe(self, candles):
        df = pd.DataFrame(candles)
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")
        df = df.sort_values("timestamp")
        df["mms_20"] = df["close"].rolling(window=20).mean().fillna(0)
        df["mms_50"] = df["close"].rolling(window=50).mean().fillna(0)
        df["mms_200"] = df["close"].rolling(window=200).mean().fillna(0)
        return df

    def populate_database(self, pair, df):
        for _, row in df.iterrows():
            aware_timestamp = timezone.make_aware(row["timestamp"], timezone.get_default_timezone())

            CurrencyData.objects.update_or_create(
                pair=pair,
                timestamp=aware_timestamp,
                defaults={
                    "mms_20": row["mms_20"],
                    "mms_50": row["mms_50"],
                    "mms_200": row["mms_200"],
                },
            )
