from django.db.models import F
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
        cur_state = auction.status
        nex_state = None
        if auction.date_start <= now <= auction.date_end:
            nex_state = "go"
        if auction.date_end < now:
            nex_state = "stop"
        if auction.date_start > now:
            nex_state = "soon"
        if cur_state == nex_state:
            continue

        auction.status = nex_state
        auction.save(update_fields=['status'])


# function to search winners in all auctions, where status is stop
@job
def search_winners():
    end_auctions = Auction.objects.filter(status="stop").exclude(
        bids__isnull=False)
    logger.info("Search winners...")
    for auction in end_auctions:
        winner = Winner.objects.filter(auction=auction)
        if winner is not None:
            continue
        winner = auction.bids.filter(auction=auction).order_by("-created_at").first()
        if winner:
            winn = winner.user
            Winner.objects.update_or_create(auction=auction, user=winn)
            logger.info(f"For Auction id: {auction.id} - winner: user_id {winner.id}")
