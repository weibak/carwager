import django_rq
import logging
from django.core.management.base import BaseCommand
from django.utils import timezone
from auction.tasks import search_winners

scheduler = django_rq.get_scheduler('default')

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Run winners search"

    def handle(self, *args, **options):
        scheduler.schedule(timezone.now(), search_winners, interval=10)
        logger.info("Scheduler works with winners")
