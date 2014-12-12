import sys
from django.core.management.base import BaseCommand, CommandError
from onyxlog.core.cron_defs import execCronTasks

class Command(BaseCommand):
    help="Executa todas as tarefas que estao presentes no arquivo cron_defs"

    def handle(self, *args, **options):
        try:
            execCronTasks()
        except Exception as e:
            raise CommandError(sys.exc_info()[0])

        self.stdout.write('Successfully')