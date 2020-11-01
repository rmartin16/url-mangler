from django import forms
from url_mangler.apps.url_mapper.models import UrlMapping


class UrlMappingForm(forms.ModelForm):
    destination_url = forms.CharField()

    class Meta:
        model = UrlMapping
        fields = ["destination_url"]
