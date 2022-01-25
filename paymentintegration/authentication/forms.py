from django import forms
from django.contrib.auth.forms import UserCreationForm
# from captcha.fields import CaptchaField
from cities_light.models import Country
from cities_light.models import City
from dal import autocomplete
from .models import User
import re

class SingupForm(UserCreationForm):
    country = forms.ModelChoiceField(queryset=Country.objects.all(), required='true')
    class Meta:
        model = User
        fields = ('email', 'country', 'city')
        widgets = {
            'city': autocomplete.ModelSelect2(url='city-autocomplete',
                                                       forward=['country'], attrs={'class':'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super(SingupForm, self).__init__(*args, **kwargs)
        del self.fields['email']

    def save(self, commit=True):
        new_user = self.instance.email
        if re.match(r'^[(a-z0-9\_\-\.)]+@[(a-z0-9\_\-\.)]+\.[(a-z)]{2,15}$', new_user.lower()):
            self.instance.email = self.instance.email
        else:
            self.instance.email = None
        return super(SingupForm, self).save(commit=commit)
