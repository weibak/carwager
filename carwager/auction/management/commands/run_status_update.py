import django_rq
import logging

from django.core.management.base import BaseCommand
from django.utils import timezone

from auction.tasks import run_status_update


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Register status update scheduled job"

    def handle(self, *args, **options):
        scheduler = django_rq.get_scheduler("default")

        job_id = "run-status-update"

        scheduler.cancel(job_id)

        scheduler.schedule(
            scheduled_time=timezone.now(),
            func=run_status_update,
            interval=10,
            id=job_id,
        )

        logger.info("Status update scheduled")
