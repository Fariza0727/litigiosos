from django.shortcuts import render
from django.views.generic import ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from .models import Content
from django.urls import reverse
from django.urls import reverse_lazy
from .forms import ContentForm
from django.http import HttpResponse, HttpResponseRedirect
from paymentintegration.authentication.models import User

# Create your views here.
class Dashboard(LoginRequiredMixin,TemplateView):
    model = Content
    template_name = "website/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super(Dashboard, self).get_context_data(**kwargs)
        if self.request.user.is_staff == True:
            contents = Content.objects.all().count()
            content_approved = Content.objects.filter(approved=True).count()
            content_pending = Content.objects.filter(approved=False).count()
            context['credit'] = self.request.user.credit
        else:
            contents = Content.objects.filter(user_id=self.request.user.id).count()
            content_approved = Content.objects.filter(user_id=self.request.user.id, approved=True).count()
            content_pending = Content.objects.filter(user_id=self.request.user.id, approved=False).count()
            context['credit'] = self.request.user.credit

        context['contents'] = contents
        context['content_approved'] = content_approved
        context['content_pending'] = content_pending
        

        return context

class ContentList(LoginRequiredMixin,TemplateView):
    model = Content
    template_name = "website/content.html"

    def get_context_data(self, **kwargs):
        context = super(ContentList, self).get_context_data(**kwargs)
        content_list = Content.objects.filter(approved=True, user_id=self.request.user.pk).order_by('-date')
        context['content_list'] = content_list
        is_ok = self.request.GET.get("ok","")
        if is_ok == "1":
            context["just_posted"] = True
        else:
            context["just_posted"] = False

        return context

class ContentCreate(LoginRequiredMixin,CreateView):
    model = Content
    form_class = ContentForm
    template_name = "website/create_content.html"

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/content/?ok=1')

        return render(request, self.template_name, {'form': form})  

class ContentUpdate(LoginRequiredMixin,UpdateView):
    model = Content
    form_class = ContentForm
    template_name = "website/update_content.html"
    success_url = reverse_lazy('content')

class ContentDetail(LoginRequiredMixin,DetailView):
    model = Content
    template_name = "website/content-detail.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        content_pk = self.kwargs.get('pk')
        context['content_detail'] = Content.objects.get(pk=content_pk)
        
        return context

class ContentPending(LoginRequiredMixin,TemplateView):
    model = Content
    template_name = "website/pend_content.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['content_list'] = Content.objects.filter(approved=False, user_id=self.request.user.id).order_by('-date')

        return context

        

