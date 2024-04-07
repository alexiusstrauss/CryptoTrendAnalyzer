import logging

from django.core.management.base import BaseCommand, CommandError
from src.apps.market_trends.models import ExecutionLog
from src.apps.market_trends.services import CurrencyDataService

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Verifica se há algum dia sem registro nos últimos 365 dias."

    def handle(self, *args, **kwargs):  # sourcery skip: extract-method
        MSG_WARNING = "Dias sem registros detectados nos últimos 365 dias:"
        try:
            if days_without_record := CurrencyDataService.check_days_without_records():
                log_msg = f"{MSG_WARNING} {days_without_record}"
                log_status = 500
                self.stdout.write(self.style.ERROR(log_msg))
                logger.warning(log_msg)
                log_entry = ExecutionLog(status=log_status, log=log_msg)
                log_entry.save()
            else:
                self.stdout.write(self.style.SUCCESS("Não há dados ausentes nos últimos 365 dias"))
        except Exception as e:
            raise CommandError(f"Erro ao verificar dias sem registros: {e}") from e
