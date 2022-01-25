from django.urls import path
from django.conf.urls import url
from .views import Dashboard, ContentList, ContentCreate, ContentUpdate, ContentDetail, ContentPending

urlpatterns = [
    url(r'^dashboard/$', Dashboard.as_view(), name='dashboard'),
    url(r'^content/$', ContentList.as_view(), name='content'),
    url(r'^content-create/$', ContentCreate.as_view(), name='content_create'),
    url(r'^content-update/(?P<pk>[0-9]+)/$', ContentUpdate.as_view(), name='content_update'),
    url(r'^content-detail/(?P<pk>[0-9]+)/$', ContentDetail.as_view(), name='content_detail'),
    url(r'^content-pending/$', ContentPending.as_view(), name='content_pending'),
    
]