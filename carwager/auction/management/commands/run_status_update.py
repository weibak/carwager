import django_rq
import logging
from django.core.management.base import BaseCommand
from django.utils import timezone
from auction.tasks import run_status_update

scheduler = django_rq.get_scheduler('default')

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Run update status"

    def handle(self, *args, **options):
        scheduler.schedule(timezone.now(), run_status_update, interval=60*60)
        logger.info("Scheduler works")
