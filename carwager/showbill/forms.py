from django import forms


class CarForm(forms.Form):
    car_mark = forms.CharField(max_length=50)
    car_model = forms.CharField(max_length=50)
    engine_type = forms.ImageField(required=False)
    engine_capacity = forms.CharField(max_length=6)
    drive = forms.CharField(max_length=50)
    gear_box = forms.CharField(max_length=50)
    description = forms.CharField(max_length=350)
    image = forms.ImageField(null=True, blank=True)
    win = forms.CharField(max_length=17)
    price = forms.DecimalField(decimal_places=2, max_digits=15)
