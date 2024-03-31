from django.db import models


class CurrencyData(models.Model):
    """Return a string representation of the object.

    Returns:
        str: A string representing the object with the pair and created_at formatted as 'pair - %d/%m/%Y %H:%M:%S'.
    """

    pair = models.CharField(max_length=12, help_text="Pair of currencies (e.g., BRLBTC, BRLETH)")
    mms_20 = models.FloatField(help_text="20-day simple moving average")
    mms_50 = models.FloatField(help_text="50-day simple moving average")
    mms_200 = models.FloatField(help_text="200-day simple moving average")
    timestamp = models.DateTimeField()

    def __str__(self):
        return f"{self.pair} - {self.timestamp.strftime('%d/%m/%Y %H:%M:%S')}"
