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
    logger.info("Search winners...")

    end_auctions = Auction.objects.filter(
        status="stop",
        bids__isnull=False,
    ).distinct()
    for auction in end_auctions:
        if Winner.objects.filter(auction=auction).exists():
            continue

        last_bid = auction.bids.order_by("-created_at").first()

        if last_bid:
            Winner.objects.create(
                auction=auction,
                user=last_bid.user,
            )

            logger.info(
                f"For Auction id: {auction.id} - winner: user_id {last_bid.user.id}"
            )
