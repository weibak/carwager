from django.utils import timezone
from django_rq import job
import logging
from auction.models import Auction, Winner

logger = logging.getLogger(__name__)


# function to update auctions statuses
@job
def run_status_update():
    auctions = Auction.objects.all()
    now = timezone.now()
    logger.info(f"Time: {now}. Update statuses...")
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


# function to search winners in all auctions, where status is stop
@job
def search_winners():
    end_auctions = Auction.objects.filter(status="stop").all()
    logger.info("Search winners...")
    for auction in end_auctions:
        winner = auction.bids.filter(auction=auction).order_by("-created_at").first()
        if winner:
            winn = winner.user
            Winner.objects.update_or_create(auction=auction, user=winn)
            logger.info(winn)
