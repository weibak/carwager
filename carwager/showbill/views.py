from django.core.paginator import Paginator
from django.shortcuts import render, redirect
import logging

from django.views.generic import TemplateView

from showbill.forms import CarFiltersForm
from showbill.models import Advert
from showbill.queries import filter_cars

logger = logging.getLogger(__name__)


class CarView(TemplateView):
    template_name = "showbill/car_list.html"

    def get_context_data(self, **kwargs, ):
        cars = Advert.objects.all()
        filters_form = CarFiltersForm(self.request.GET)

        if filters_form.is_valid():
            cost__gt = filters_form.cleaned_data["cost__gt"]
            cost__lt = filters_form.cleaned_data["cost__lt"]
            order_by = filters_form.cleaned_data["order_by"]
            cars = filter_cars(cars, cost__gt, cost__lt, order_by)

        paginator = Paginator(cars, 30)
        page_number = "page"
        cars = paginator.get_page(page_number)
        return {"cars": cars, "filters_form": filters_form}
