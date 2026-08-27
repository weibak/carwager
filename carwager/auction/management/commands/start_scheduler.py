import time
import sys
from django.core.management.base import BaseCommand
from django_rq.management.commands.rqscheduler import Command as RQSchedulerCommand


class Command(RQSchedulerCommand):
    help = 'Start RQ scheduler with Redis connection retry'
    
    def add_arguments(self, parser):
        # First add parent arguments
        super().add_arguments(parser)
        
    def handle(self, *args, **options):
        max_retries = 10
        retry_delay = 5
        
        for attempt in range(max_retries):
            try:
                self.stdout.write(f'Attempt {attempt + 1}/{max_retries} to connect to Redis...')
                
                # Call parent handle method
                super().handle(*args, **options)
                return
                
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'Connection failed: {e}'))
                
                if attempt < max_retries - 1:
                    self.stdout.write(f'Retrying in {retry_delay} seconds...')
                    time.sleep(retry_delay)
                else:
                    self.stdout.write(self.style.ERROR('Max retries reached. Exiting.'))
                    sys.exit(1)