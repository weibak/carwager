import logging
from django.db.models import F
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from rest_framework.generics import get_object_or_404

from auction.forms import AuctionForm, CarAuctionForm
from auction.models import Auction, CarAuction, Bid
from auction.queries import filter_cars
from showbill.forms import CarFiltersForm

logger = logging.getLogger(__name__)


class CarAuctionView(TemplateView):
    template_name = "auction/auction_car_list.html"

    def get_context_data(self, **kwargs, ):
        auctions = Auction.objects.all()
        filters_form = CarFiltersForm(self.request.GET)

        if filters_form.is_valid():
            price__gt = filters_form.cleaned_data["price__gt"]
            price__lt = filters_form.cleaned_data["price__lt"]
            order_by = filters_form.cleaned_data["order_by"]
            engine_type = filters_form.cleaned_data["engine_type"]
            gear_box = filters_form.cleaned_data["gear_box"]
            drive = filters_form.cleaned_data["drive"]
            auctions = filter_cars(auctions, price__gt, price__lt, order_by, engine_type, gear_box, drive)

        paginator = Paginator(auctions, 30)
        page_number = "page"
        auctions = paginator.get_page(page_number)
        return {"auctions": auctions, "filters_form": filters_form}


def choise_mark(request, mark_id):
    ...


def choise_model(request, choise_mark, model_id):
    ...


def create_auction(request, *args, **kwargs):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = AuctionForm(request.POST, request.FILES)
            form_car = CarAuctionForm(request.POST)
            if form_car.is_valid():
                car = CarAuction.objects.create(**form_car.cleaned_data)
                auction = Auction.objects.create(
                    car=car, owner=request.user, engine_type=form.data.get("engine_type"),
                    engine_capacity=form.data.get("engine_capacity"), drive=form.data.get("drive"),
                    gear_box=form.data.get("gear_box"), description=form.data.get("description"),
                    image=form.data.get("image.url"), win=form.data.get("win"), price=form.data.get("price"),
                    price_usd=form.data.get("price_usd"), phone_number=form.data.get("phone_number"),
                    date_start=form.data.get("date_start"),
                    date_end=form.data.get("date_end"),
                )
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


def auction_view(request, auction_id):
    auction = get_object_or_404(Auction, id=auction_id)
    if request.method == "POST":
        if request.POST.get("bid"):
            Bid.objects.create(
                auction=auction, user=request.user, bid=request.POST.get("bid")
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
        },
    )
