from django.utils import timezone
from django_rq import job
import logging
from auction.models import Auction


logger = logging.getLogger(__name__)


@job
def run_status_update():
    auctions = Auction.objects.all()
    now = timezone.now()
    logger.info("I'm working...")
    logger.info(now)
    for auction in auctions:
        if auction.date_start <= now <= auction.date_end:
            auction.status = "go"
            auction.save()
        if auction.date_end < now:
            auction.status = "stop"
            auction.save()
        if auction.date_start > now:
            auction.status = "soon"
            auction.save()
