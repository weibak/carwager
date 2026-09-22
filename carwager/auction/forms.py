from datetime import timedelta

from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from showbill.models import DRIVE, ENGINE_TYPE, GEAR_BOX, ORDER_BY_CHOICES, CarMark, CarModel
from auction.models import STATUS_AUC

CAR_MARKS = (('', ''), *CarMark.objects.values_list('id', 'car_mark'))


class AuctionFiltersForm(forms.Form):
    price__gt = forms.IntegerField(min_value=0, label="Price Min", required=False)
    price__lt = forms.IntegerField(min_value=0, label="Price Max", required=False)
    order_price = forms.ChoiceField(choices=ORDER_BY_CHOICES, required=False)
    engine_type = forms.ChoiceField(choices=ENGINE_TYPE, required=False)
    mark = forms.ChoiceField(choices=CAR_MARKS, required=False,)
    gear_box = forms.ChoiceField(choices=GEAR_BOX, required=False)
    drive = forms.ChoiceField(choices=DRIVE, required=False)
    status = forms.ChoiceField(choices=STATUS_AUC, required=False)

    def clean(self):
        cleaned_data = super().clean()
        price__gt = cleaned_data.get("price__gt")
        price__lt = cleaned_data.get("price__lt")
        if price__gt and price__lt and price__gt > price__lt:
            raise ValidationError("Min price can't be greater than Max price")


class CarAuctionForm(forms.Form):
    mark = forms.ModelChoiceField(CarMark.objects.all(), required=True)
    model = forms.ModelChoiceField(CarModel.objects.all(), required=True)
    year = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        mark_id = kwargs.pop('mark_id', None)
        super().__init__(*args, **kwargs)
        if mark_id:
            self.fields['model'].queryset = CarModel.objects.filter(car_mark_id=mark_id)


class AuctionForm(forms.Form):
    engine_type = forms.ChoiceField(choices=ENGINE_TYPE)
    engine_capacity = forms.FloatField()
    drive = forms.ChoiceField(choices=DRIVE)
    gear_box = forms.ChoiceField(choices=GEAR_BOX)
    description = forms.CharField(max_length=500)
    image = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'multiple': True}), help_text="You can upload up to 8 photos.")
    win = forms.CharField(max_length=17, required=False)
    price = forms.DecimalField(decimal_places=2, max_digits=15)
    phone_number = forms.CharField(max_length=13)
    date_start = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={
                'type': 'datetime-local',
                'step': '3600',
                'placeholder': 'Select start date and time',
            }
        ),
        input_formats=['%Y-%m-%dT%H', '%Y-%m-%d %H', '%Y-%m-%d %H'],
        help_text='Select a future date and time for the auction start.'
    )
    date_end = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={
                'type': 'datetime-local',
                'step': '3600',
                'placeholder': 'Select end date and time',
            }
        ),
        input_formats=['%Y-%m-%dT%H', '%Y-%m-%d %H', '%Y-%m-%d %H'],
        help_text='Select a date later than the start time.'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.now = timezone.now()
        self.fields['date_start'].widget.attrs['min'] = self.now.strftime('%Y-%m-%dT%H')
        self.fields['date_end'].widget.attrs['min'] = (self.now + timedelta(hours=1)).strftime('%Y-%m-%dT%H')

    def clean(self):
        cleaned_data = super().clean() or {}
        files = self.files.getlist('image')
        if len(files) > 8:
            raise ValidationError("You can upload up to 8 photos.")

        date_start = cleaned_data.get('date_start', self.now)
        date_end = cleaned_data.get('date_end', self.now)
        if date_start and date_start <= self.now:
            raise ValidationError("Auction start date must be in the future.")
        if date_start and date_end and date_end <= date_start:
            raise ValidationError("Auction end date must be later than the start date.")

        cleaned_data['image_list'] = files
        if files:
            cleaned_data['image'] = files[0]
        return cleaned_data
