import django_rq
import logging
from django.core.management.base import BaseCommand
from django.utils import timezone
from auction.tasks import search_winners

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Run winners search"

    def handle(self, *args, **options):
        scheduler = django_rq.get_scheduler("default")
        job_id = "run-search-winners"
        scheduler.cancel(job_id)

        scheduler.schedule(
            scheduled_time=timezone.now(),
            func=search_winners,
            interval=10,
            id=job_id,
        )        
        logger.info("Scheduler works with winners")
