from django import forms

from auction.models import CarMarkAuction, CarModelAuction
from showbill.models import DRIVE, ENGINE_TYPE, GEAR_BOX


class CarAuctionForm(forms.Form):
    mark = forms.ModelChoiceField(CarMarkAuction.objects.all(), required=True)
    model = forms.ModelChoiceField(CarModelAuction.objects.all())
    year = forms.IntegerField()


class AuctionForm(forms.Form):
    engine_type = forms.ChoiceField(choices=ENGINE_TYPE)
    engine_capacity = forms.FloatField()
    drive = forms.ChoiceField(choices=DRIVE)
    gear_box = forms.ChoiceField(choices=GEAR_BOX)
    description = forms.CharField(max_length=500)
    image = forms.ImageField(required=False)
    win = forms.CharField(max_length=17, )
    price = forms.DecimalField(decimal_places=2, max_digits=15)
    price_usd = forms.DecimalField(decimal_places=2, max_digits=15)
    phone_number = forms.CharField(max_length=13)
    date_start = forms.DateTimeField(input_formats='%Y-%m-%d %H:%M', help_text='2022-03-19 14:30')
    date_end = forms.DateTimeField(input_formats='%Y-%m-%d %H:%M', help_text='2022-03-19 14:30')
"""
    def clean_date_start(self):
        date_start = self.cleaned_data['date_start']
        date_start = datetime.strptime(date_start, format="%d/%m/%Y %H:%M")
        return date_start

    def clean_date_end(self):
        date_end = self.cleaned_data['date_end']
        date_end = datetime.strptime(date_end, format="%d/%m/%Y %H:%M")
        return date_end
"""