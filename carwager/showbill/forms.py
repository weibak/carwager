from django import forms


class CarForm(forms.Form):
    mark = forms.CharField(max_length=50)
    model = forms.CharField(max_length=50)
    year = forms.IntegerField()
