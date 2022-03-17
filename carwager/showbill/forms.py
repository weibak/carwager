from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError

from showbill.models import ORDER_BY_CHOICES, DRIVE, ENGINE_TYPE, GEAR_BOX


class CarFiltersForm(forms.Form):
    price__gt = forms.IntegerField(min_value=0, label="Price Min", required=False)
    price__lt = forms.IntegerField(min_value=0, label="Price Max", required=False)
    order_by = forms.ChoiceField(choices=ORDER_BY_CHOICES, required=False)

    def clean(self):
        cleaned_data = super().clean()
        price__gt = cleaned_data.get("price__gt")
        price__lt = cleaned_data.get("price__lt")
        if price__gt and price__lt and price__gt > price__lt:
            raise ValidationError("Min price can't be greater than Max price")


class AdvertFiltersForm(forms.Form):
    order_by = forms.ChoiceField(
        choices=(
            ("-created_at", "Newest First"),
            ("created_at", "Oldest First"),),
        required=False,
    )


class AdvertForm(forms.Form):
    car = forms.CharField(max_length=100)
    engine_type = forms.CharField(max_length=100, )
    engine_capacity = forms.IntegerField()
    drive = forms.CharField(max_length=100,)
    gear_box = forms.CharField(max_length=100, )
    description = forms.CharField(max_length=500)
    image = forms.ImageField()
    win = forms.CharField(max_length=17,)
    price = forms.DecimalField(decimal_places=2, max_digits=15)
    price_usd = forms.DecimalField(decimal_places=2, max_digits=15)
    phone_number = forms.CharField(max_length=13)
