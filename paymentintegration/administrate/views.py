from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from paymentintegration.website.models import Content
from django.http import HttpResponse
from paymentintegration.authentication.models import User
# Create your views here.

class DashboardAdmin(LoginRequiredMixin, ListView):
    model = Content
    template_name = "admin/dashboard_admin.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['content_list'] = Content.objects.all().order_by('-date')

        return context

class UserinfoAdmin(LoginRequiredMixin, ListView):
    model = User
    template_name = "admin/register_users.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_list'] = User.objects.all().order_by('-date_joined')

        return context

def ApproveContent(request):
    my_id = request.POST.get('value')
    Content.objects.filter(id=my_id).update(approved=True)
    contentuser = Content.objects.get(pk=my_id)
    user = User.objects.get(pk=contentuser.user_id)
    if user.credit is None:
        user.credit = 5
    else:
        user.credit += 5
    user.save()

    return HttpResponse('Ok')