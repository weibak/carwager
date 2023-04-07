from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
import logging
from django.contrib import messages
from django.views.generic import TemplateView

from showbill.forms import CarFiltersForm, AdvertForm, CarForm, AdvertFiltersForm
from showbill.models import Advert, Car
from showbill.queries import filter_cars, filter_adverts

logger = logging.getLogger(__name__)


# view for show all adverts on the showbill
class CarView(TemplateView):
    template_name = "showbill/car_list.html"

    def get_context_data(self, **kwargs, ):
        adverts = Advert.objects.all()
        filters_form = CarFiltersForm(self.request.GET)
        car_date = AdvertFiltersForm(self.request.GET)

        if filters_form.is_valid():
            price__gt = filters_form.cleaned_data["price__gt"]
            price__lt = filters_form.cleaned_data["price__lt"]
            mark = filters_form.cleaned_data["mark"]
            order_price = filters_form.cleaned_data["order_price"]
            engine_type = filters_form.cleaned_data["engine_type"]
            gear_box = filters_form.cleaned_data["gear_box"]
            drive = filters_form.cleaned_data["drive"]
            adverts = filter_cars(adverts, price__gt, price__lt, order_price, mark, engine_type, drive, gear_box)

        if car_date.is_valid():
            order_date = car_date.cleaned_data["order_date"]
            adverts = filter_adverts(adverts, order_date)
        # settings of page size
        paginator = Paginator(adverts, 30)
        page_number = "page"
        adverts = paginator.get_page(page_number)
        return {"adverts": adverts, "filters_form": filters_form, "date_filter": car_date}


def create_advert(request, *args, **kwargs):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = AdvertForm(request.POST, request.FILES)
            form_car = CarForm(request.POST, )
            if form_car.is_valid():
                car = Car.objects.create(**form_car.cleaned_data)
                if form.is_valid():
                    logger.info(form.cleaned_data)
                    advert = Advert.objects.create(car=car, owner=request.user, **form.cleaned_data)
                    advert.save()
                return redirect(
                    "/",
                )
        else:
            form = AdvertForm()
            form_car = CarForm()
            return render(request, "showbill/create_advert.html", {"form": form, "form_car": form_car})
    else:
        return redirect("auth")


# show current advert
def advert_view(request, advert_id):
    advert = get_object_or_404(Advert, id=advert_id)
    if request.method == "POST":
        if request.user.is_authenticated and request.method == "POST":
            if request.POST["action"] == "add":
                advert.favorites.add(request.user)
                messages.info(request, "Car successfully added to favorites")
            elif request.POST["action"] == "remove":
                advert.favorites.remove(request.user)
                messages.info(request, "Car successfully removed to favorites")
            redirect("car_details", advert_id=advert.id)
    return render(
        request,
        "showbill/car_details.html",
        {
            "advert": advert,
            "is_advert_in_favorites": request.user in advert.favorites.all(),
        },
    )
