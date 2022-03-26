import logging
import datetime
from django.db.models import F
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.generic import TemplateView
from rest_framework.generics import get_object_or_404
from auction.forms import AuctionForm, CarAuctionForm, AuctionFiltersForm
from auction.models import Auction, CarAuction, Bid, Winner
from auction.queries import filter_cars_auction

logger = logging.getLogger(__name__)


# general page of auctions, auctions going, auctions ended, auctions soon, filter-forms.
class CarAuctionView(TemplateView):
    template_name = "auction/auction_car_list.html"

    def get_context_data(self, **kwargs, ):
        auctions = Auction.objects.all()
        filters_form = AuctionFiltersForm(self.request.GET)

        if filters_form.is_valid():
            price__gt = filters_form.cleaned_data["price__gt"]
            price__lt = filters_form.cleaned_data["price__lt"]
            order_by = filters_form.cleaned_data["order_by"]
            engine_type = filters_form.cleaned_data["engine_type"]
            gear_box = filters_form.cleaned_data["gear_box"]
            drive = filters_form.cleaned_data["drive"]
            status = filters_form.cleaned_data["status"]
            auctions = filter_cars_auction(
                auctions, price__gt, price__lt, order_by, engine_type, gear_box, drive, status
            )

        paginator = Paginator(auctions, 30)
        page_number = "page"
        auctions = paginator.get_page(page_number)
        return {"auctions": auctions, "filters_form": filters_form}


# view to create auction
def create_auction(request, *args, **kwargs):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = AuctionForm(request.POST, request.FILES)
            form_car = CarAuctionForm(request.POST)
            now = str(timezone.now())  # time to compare statuses
            if form_car.is_valid():
                car = CarAuction.objects.create(**form_car.cleaned_data)
                if form.is_valid():
                    # take status to auction advert
                    status = ""
                    if request.POST.get("date_start") <= now <= request.POST.get("date_end"):
                        status = "go"
                    if request.POST.get("date_end") < now:
                        status = "stop"
                    if request.POST.get("date_start") > now:
                        status = "soon"
                    auction = Auction.objects.create(
                        car=car, owner=request.user, status=status, **form.cleaned_data
                    )  # create auction in DB
                    auction.save()
                return redirect(
                    "auction",
                )
        else:
            form = AuctionForm()
            form_car = CarAuctionForm()
            return render(request, "auction/create_auction.html", {
                "form": form, "form_car": form_car})
    else:
        return redirect("auth")


# details of auction, info, bids, take bid
def auction_view(request, auction_id):
    auction = get_object_or_404(Auction, id=auction_id)
    time = datetime.datetime.now()
    winn = Winner.objects.filter(auction=auction).first()  # search winners of auction
    winner = ""
    if winn is not None:
        winner = winn.user
    if request.method == "POST":
        if request.POST.get("bid"):
            # try to do validate of bid. if two user take a bid from one start price
            bids = Bid.objects.filter(auction=auction, bef_bid_price=auction.price).all()
            if bids.exists():
                messages.info(request, "Oops... Update price, and take a new bid")
                redirect("auction_details", auction_id=auction.id)
            else:
                Bid.objects.create(
                    auction=auction, user=request.user, bid=request.POST.get("bid"), bef_bid_price=auction.price
                )
                Auction.objects.filter(id=auction_id).update(price=F("price") + request.POST.get("bid"))
            return redirect("auction_details", auction_id=auction_id)
        if request.user.is_authenticated and request.method == "POST":
            if request.POST["action"] == "add":
                auction.favorites.add(request.user)
                messages.info(request, "Auction successfully added to favorites")
            elif request.POST["action"] == "remove":
                auction.favorites.remove(request.user)
                messages.info(request, "Auction successfully removed to favorites")
            redirect("auction_details", auction_id=auction.id)
    return render(
        request,
        "auction/auction_details.html",
        {
            "auction": auction,
            "is_auction_in_favorites": request.user in auction.favorites.all(),
            "bids": auction.bids.order_by("-created_at")[0:10],
            "time": time,
            "winner": winner,
        },
    )
