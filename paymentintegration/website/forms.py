from django import forms
from cities_light.models import Country
from cities_light.models import City
from dal import autocomplete
from paymentintegration.website.models import Content

class ContentForm(forms.ModelForm):
    country = forms.ModelChoiceField(queryset=Country.objects.all(), required='true')
    class Meta:
        model = Content
        fields = ('title', 'username', 'surname', 'description', 'country', 'city', 'category', 'voting', 'user')
        widgets = {
            'city': autocomplete.ModelSelect2(url='city-autocomplete',
                                                       forward=['country'])
        }
