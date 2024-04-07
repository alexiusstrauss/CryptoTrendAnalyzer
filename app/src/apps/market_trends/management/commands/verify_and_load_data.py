import logging

from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.utils import timezone
from src.apps.market_trends.models import ExecutionLog

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Verifica se houve um registro de sucesso hoje e, se não, executa o load_market_data."

    def handle(self, *args, **kwargs):
        today = timezone.now().date()
        try:
            logs_today = ExecutionLog.objects.filter(created_at__date=today, status=200)

            if not logs_today.exists():
                self.stdout.write(
                    self.style.WARNING("Nenhum carga de dados encontrado para hoje. Iniciando load_market_data...")
                )
                logger.warning("Não foi encontrado registro de carga de dados no dia de hoje")
                call_command("load_market_data")
            else:
                self.stdout.write(self.style.SUCCESS("Dados atualizados na data de hoje. Nenhuma ação necessária."))

        except Exception as e:
            error_message = f"Erro ao verificar registros de carga de dados: {e}"
            self.stdout.write(self.style.ERROR(error_message))
            logger.error(error_message)
