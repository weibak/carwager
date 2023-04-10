from django import forms


class AddNewForm(forms.Form):
    title = forms.CharField(max_length=200)
    image = forms.FileField()
    slug = forms.SlugField(max_length=200)
    text = forms.CharField(label="text for new article", widget=forms.Textarea)
