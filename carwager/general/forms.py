from django import forms


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=100)
    first_name = forms.CharField(max_length=200)
    last_name = forms.CharField(max_length=200)
    email = forms.EmailField()
    password = forms.CharField(min_length=8, widget=forms.PasswordInput())
    age = forms.IntegerField(min_value=18, required=False)


class AuthForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(min_length=8, widget=forms.PasswordInput())
