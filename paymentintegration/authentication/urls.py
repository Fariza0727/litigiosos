from django.conf.urls import url
from .views import LoginView
from .views import LogoutView, SingupView, CityAutocomplete, activateAccount

urlpatterns = [
               url(r'^login/$', LoginView.as_view(), name='view_login'),
               url(r'^logout/$', LogoutView.as_view(), name='view_logout'),
               url(r'^signup/$', SingupView.as_view(), name='view_singup'),
               url(r'^city-autocomplete/$', CityAutocomplete.as_view(create_field='name'), name='city-autocomplete'),
               url(r'^activate/(?P<uidb64>.+)/(?P<token>.+)/$',activateAccount, name='activateaccount'),
              ]