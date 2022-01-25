from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse, reverse_lazy
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import FormView, RedirectView
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.edit import CreateView
from .models import User
from .forms import SingupForm
from dal import autocomplete
from cities_light.models import Country
from cities_light.models import City
import re 
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.template import RequestContext
from paymentintegration.authentication.email import send_mail

class LoginView(FormView):
    form_class = AuthenticationForm
    template_name = "authentication/signin.html"
    
    def get_success_url(self):
        return reverse_lazy("land")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(LoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())

        return super(LoginView, self).form_valid(form)


class LogoutView(RedirectView):
    url = '/login/'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)

class SingupView(CreateView):
    model = User
    form_class = SingupForm
    template_name = 'authentication/signup.html'
    success_url = reverse_lazy('view_login')

    extra_context = {}


    # def get_context_data(self, **kwargs):
    #     context = super(SingupView, self).get_context_data(**kwargs)

    #     for k in self.extra_context.keys():
    #         context[k] = self.extra_context[k]  

    #     return context



    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        email = request.POST.get('email')

        if form.is_valid():
            user = form.save(commit=False)
            user.email= email
            user.username = email
            user.is_active = False
            try:
                user.save()

            
                mail_subject = "Bienvenido a Litigiosos.com!"
                mail_context = {
                    'email_title': "Bienvenido a Litigiosos.com",
                    'email_body': "Utiliza este email para activar tu cuenta, y empezar a trabajar con nuestra plataforma.",
                    'user': user,
                    'site_url': request._current_scheme_host,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                }

                send_mail(mail_subject, email_template_name=None,
                                context=mail_context, to_email=[user.email],
                                html_email_template_name='authentication/register_email.html')
                
                messages.success(request, "Revise su bandeja de entrada de correo para activar la cuenta !!")
                self.extra_context["status"] = True
                return render(request, "authentication/signup.html")


            except:
                self.extra_context["status"] = False
                messages.error(request, "Error creando el usuario, prueba otro email.")
                return self.render_to_response(self.get_context_data(form=form))

        else:
            self.extra_context["status"] = False
            return self.render_to_response(self.get_context_data(form=form))

class CityAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = City.objects.all()
        country = self.forwarded.get('country', None)
        if country:
            qs = qs.filter(country=country)
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs

def activateAccount(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None  and default_token_generator.check_token(user, token):
        user.is_active = True
        if user.credit is None:
            user.credit = 5
        else:
            user.credit += 5
        user.save()
        login(request, user,backend="django.contrib.auth.backends.ModelBackend")
        messages.success(request, "Su cuenta ha sido Validada!")
        return redirect('/')
    else:
        return HttpResponse('Activation link is invalid!')