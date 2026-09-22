import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView

from showbill.forms import AdvertFiltersForm, AdvertForm, CarFiltersForm, CarForm
from showbill.models import Advert, AdvertImage, Car
from showbill.models import CarModel
from showbill.queries import filter_adverts, filter_cars

logger = logging.getLogger(__name__)


# view for show all adverts on the showbill
@method_decorator(cache_page(60), name="dispatch")
class CarView(TemplateView):
    template_name = "showbill/car_list.html"

    def get_context_data(self, **kwargs, ):
        adverts = Advert.objects.all().order_by("-created_at")
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


# crete advert on showbill view
@login_required
def create_advert(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("auth")

    if request.method == "POST":
        form = AdvertForm(request.POST, request.FILES)
        # supply mark_id so model choices are validated server-side
        form_car = CarForm(request.POST, mark_id=request.POST.get("mark"))
        if form_car.is_valid():
            car = Car.objects.create(**form_car.cleaned_data)
            if form.is_valid():
                cleaned_data = form.cleaned_data.copy()
                uploaded_files = cleaned_data.pop("image_list", [])
                advert_data = {key: value for key, value in cleaned_data.items() if key != "image"}
                advert = Advert.objects.create(
                    car=car,
                    owner=request.user,
                    **advert_data,
                )
                for image in uploaded_files[:8]:
                    AdvertImage.objects.create(advert=advert, image=image)
                logger.info("Advert created with %s uploaded images", len(uploaded_files))
            return redirect("showbill")
        else:
            # if car form invalid, re-render with posted data and mark-specific models
            form = AdvertForm(request.POST)
            form_car = CarForm(request.POST, mark_id=request.POST.get("mark"))
            return render(request, "showbill/create_advert.html", {"form": form, "form_car": form_car})

    else:
        form = AdvertForm()
        form_car = CarForm()
        return render(request, "showbill/create_advert.html", {"form": form, "form_car": form_car})


# show current advert
@cache_page(60 * 15)
def advert_view(request, advert_id):
    advert = get_object_or_404(Advert, id=advert_id)
    if request.method == "POST":
        action = request.POST["action"]
        if request.user.is_authenticated:
            if action == "add":
                advert.favorites.add(request.user)
                messages.info(request, "Car successfully added to favorites")
            elif action == "remove":
                advert.favorites.remove(request.user)
                messages.info(request, "Car successfully removed to favorites")
            redirect("car_details", advert_id=advert.id)
    return render(
        request,
        "showbill/car_details.html",
        {
            "advert": advert,
            "is_advert_in_favorites": advert.favorites.filter(id=request.user.id).exists(),
        },
    )


def models_for_mark(request, mark_id):
    models = list(CarModel.objects.filter(car_mark_id=mark_id).values("id", "car_model"))
    return JsonResponse(models, safe=False)
