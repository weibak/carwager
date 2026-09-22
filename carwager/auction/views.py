import logging

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView
from rest_framework.generics import get_object_or_404

from auction.forms import AuctionFiltersForm, AuctionForm, CarAuctionForm
from auction.models import Auction, AuctionImage, Winner
from auction.queries import filter_cars_auction
from showbill.models import Car, CarModel

logger = logging.getLogger(__name__)


# general page of auctions, auctions going, auctions ended, auctions soon, filter-forms.
@method_decorator(cache_page(60), name="dispatch")
class CarAuctionView(TemplateView):
    template_name = "auction/auction_car_list.html"

    def get_context_data(self, **kwargs, ):
        logger.info("Auctions page opened")

        auctions = Auction.objects.all().order_by("-created_at")
        filters_form = AuctionFiltersForm(self.request.GET)
        # validate filter form
        if filters_form.is_valid():
            price__gt = filters_form.cleaned_data["price__gt"]
            price__lt = filters_form.cleaned_data["price__lt"]
            order_price = filters_form.cleaned_data["order_price"]
            engine_type = filters_form.cleaned_data["engine_type"]
            gear_box = filters_form.cleaned_data["gear_box"]
            drive = filters_form.cleaned_data["drive"]
            status = filters_form.cleaned_data["status"]
            mark = filters_form.cleaned_data["mark"]
            auctions = filter_cars_auction(
                auctions, price__gt, price__lt, order_price, engine_type, drive, gear_box, status, mark
            )
        # settings of page size
        paginator = Paginator(auctions, 30)
        page_number = "page"
        auctions = paginator.get_page(page_number)
        logger.info("Auctions loaded")

        return {"auctions": auctions, "filters_form": filters_form}


# AJAX endpoint for auction models
def models_for_mark_auction(request, mark_id):
    models = list(CarModel.objects.filter(car_mark_id=mark_id).values("id", "car_model"))
    return JsonResponse(models, safe=False)


# view to create auction
@login_required
def create_auction(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("auth")

    if request.method == "POST":
        form = AuctionForm(request.POST, request.FILES)
        form_car = CarAuctionForm(request.POST, mark_id=request.POST.get("mark"))
        now = str(timezone.now())  # time to compare statuses
        if form_car.is_valid():
            # create or get canonical Car from showbill models
            mark = form_car.cleaned_data["mark"]
            model = form_car.cleaned_data["model"]
            year = form_car.cleaned_data["year"]
            car, _created = Car.objects.get_or_create(mark=mark, model=model, defaults={"year": year})
            if not _created and car.year != year:
                # if existing car has different year, update if desired (keep existing to avoid duplicates)
                car.year = year
                car.save()

            if form.is_valid():
                cleaned_data = form.cleaned_data.copy()
                uploaded_files = cleaned_data.pop("image_list", [])
                auction_data = {key: value for key, value in cleaned_data.items() if key != "image"}
                status = ""
                if request.POST.get("date_start") <= now <= request.POST.get("date_end"):
                    status = "go"
                if request.POST.get("date_end") < now:
                    status = "stop"
                if request.POST.get("date_start") > now:
                    status = "soon"
                auction = Auction.objects.create(
                    car=car,
                    owner=request.user,
                    status=status,
                    **auction_data,
                )
                for image in uploaded_files[:8]:
                    AuctionImage.objects.create(auction=auction, image=image)
                auction.save()
            return redirect(
                "auction",
            )
        else:
            form = AuctionForm(request.POST)
            form_car = CarAuctionForm(request.POST, mark_id=request.POST.get("mark"))
            return render(request, "auction/create_auction.html", {"form": form, "form_car": form_car})

    else:
        form = AuctionForm()
        form_car = CarAuctionForm()
        return render(request, "auction/create_auction.html", {
            "form": form, "form_car": form_car})


# details of auction, info, bids, take bid
def auction_view(request, auction_id):
    auction = get_object_or_404(Auction, id=auction_id)
    winner = winn.user.username if (winn := Winner.objects.filter(auction=auction).first()) else "No winner"

    if request.method == "POST" and request.user.is_authenticated and request.POST.get("bid"):
        from .bid_processor import process_bid_with_retry

        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to place a bid.")
            return redirect("auction_details", auction_id=auction_id)

        if auction.owner_id == request.user.id:
            messages.error(request, "You can't bid on your own auction.")
            return redirect("auction_details", auction_id=auction_id)

        bid_amount_str = request.POST.get("bid")

        # Use atomic bid processor with retry
        success, message, new_price, _ = process_bid_with_retry(
            auction_id=auction_id,
            user_id=request.user.id,
            bid_amount_str=bid_amount_str,
            max_retries=3
        )

        if success:
            # Refresh auction to get updated price
            auction.refresh_from_db()

            # Send WebSocket update to all connected clients
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f"auction_{auction.id}",
                {
                    "type": "price_update",
                    "new_price": new_price,
                    "auction_id": auction.id,
                }
            )

            messages.success(request, "Bid placed successfully!")
        else:
            messages.error(request, message)

        if request.POST["action"] == "add":
            auction.favorites.add(request.user)
            messages.info(request, "Auction successfully added to favorites")
        elif request.POST["action"] == "remove":
            auction.favorites.remove(request.user)
            messages.info(request, "Auction successfully removed to favorites")
        return redirect("auction_details", auction_id=auction_id)

    return render(
        request,
        "auction/auction_details.html",
        {
            "auction": auction,
            "is_auction_in_favorites": request.user in auction.favorites.all(),
            "bids": auction.bids.order_by("-created_at")[0:10],
            "winner": winner,
        },
    )
