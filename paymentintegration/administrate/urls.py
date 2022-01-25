from django.urls import path
from django.conf.urls import url
from .views import DashboardAdmin, ApproveContent, UserinfoAdmin

urlpatterns = [
    url(r'^review-admin/$', DashboardAdmin.as_view(), name='review_admin'),
    url(r'^review-admin-users/$', UserinfoAdmin.as_view(), name='review_admin_users'), 
    url(r'^approve_content/$', ApproveContent, name='approve_content'), 
]