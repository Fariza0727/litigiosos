from django.shortcuts import render
from django.views.generic import TemplateView
from paymentintegration.website.models import Content
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from paymentintegration.authentication.models import User
from paymentintegration.website.models import Rating, Commit, ContentView
import json
from cities_light.models import Country
from django.db.models import Q

from cities_light.models import City
from django.http import HttpResponse
from django.views.generic.detail import DetailView
# Create your views here.

class LandPage(TemplateView):
    template_name = "land/index.html"


class TerminosYCondiciones(TemplateView):
    template_name = "land/tic.html"
        
class ArticleList(LoginRequiredMixin, TemplateView):
    template_name = "land/article.html"
    model = Content

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        contents = Content.objects.filter(approved=True)
        for c in contents:
            counter = 0
            total = 0
            
            rating = Rating.objects.filter(content_id=c.pk)
            for r in rating:
                total += r.marks
                counter += 1
                my_value = 0
            if counter == 0:
                total = 0
                counter = 1
                c.counter = counter - 1
            else:
                c.counter = counter
            if total % counter == 0:
                my_value = total / counter
            else:
                if type(total / counter) == float:
                    my_value = int(total / counter) + 0.5
                else:
                    my_value = total / counter

            c.marks = my_value
            review = ContentView.objects.filter(content_id=c.pk, user_id=self.request.user.id)
            if review.exists():
                c.view = True
            else:
                c.view = False
        print("++", contents)
        paginator = Paginator(contents, 10)
        page = self.request.GET.get('page')
        page_obj = paginator.get_page(page)
        context['content_list'] = page_obj
        context["empty_search"] = True
        return context

class ArticleDetail(LoginRequiredMixin,DetailView):
    model = Content
    template_name = "land/article-detail.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        content_pk = self.kwargs.get('pk')
        context['article_detail'] = Content.objects.get(pk=content_pk)
        context['article_commit'] = Commit.objects.filter(content_id=content_pk)
        context['commit_count'] = Commit.objects.filter(content_id=content_pk).count()
        rating_total = Rating.objects.filter(content_id = content_pk)
        total = 0
        count_user = 0
        for rat in rating_total:
            total += rat.marks
            count_user += 1
            count_user_real = True
            my_value = 0
        if count_user == 0:
            total = 0
            count_user = 1
            count_user_real = False
        if total % count_user == 0:
            my_value = total / count_user
        else:
            if type(total / count_user) == float:
                my_value = int(total / count_user) + 0.5
            else:
                my_value = total / count_user

        context['rating_total'] = total
        if count_user_real == False:
            context['rating_users'] = 0
        else:
            context['rating_users'] = count_user

        context['rating_avr'] = total / count_user
        context['rating_content'] = my_value
        return context
    
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            rating_content = request.POST.get('ratingPoints')
            if rating_content < '0':
                rating_content = 0
            elif rating_content > '5':
                rating_content = 5
            else:
                rating_content = rating_content

            id_content = Content.objects.get(id=request.POST.get('postID'))
            user_rating = User.objects.get(id=request.user.id)

            query_rating = Rating.objects.filter(
                user=user_rating, content=id_content)
            my_content = 0

            if query_rating:
                for q in query_rating:
                    my_content = q.id
                rating_save = Rating.objects.get(id=my_content)
                rating_save.marks = rating_content
                rating_save.save()
            # Creating
            else:
                object_rating = Rating(
                    user=user_rating, content=id_content, marks=rating_content)
                object_rating.save()
            return HttpResponse('ok')
        else:
            return HttpResponse('no')

def autocompleteModelSearch(request):
    if request.is_ajax():
        q = request.GET.get('phrase', '').capitalize()
        search_qs = Content.objects.filter(username__startswith=q)
        results = []
        for r in search_qs:
            results.append(r.username + " " + r.surname)
        data = json.dumps(list(set(results)))
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

def autocompleteModelSearchCountry(request):
    if request.is_ajax():
        q = request.GET.get('phrase1', '').capitalize()
        search_country = Country.objects.filter(name__startswith=q)
        results = []
        for r_country in search_country:
            search_city = City.objects.filter(country_id=r_country.pk)
            for r_city in search_city:
                results.append(r_country.name_ascii + " " + r_city.name_ascii)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def NewSearchContent(request, username):
    username_val = username.split(" ")[0]

    qq = Q(username__icontains=username_val)
    try:
        surname = username.split(" ")[1]
        qq = qq &  Q(surname__icontains=surname)
    except:
        qq = qq |  Q(surname__icontains=username_val)

    contents = Content.objects.filter(qq).filter(approved=True)
    print("==============",contents)
    paginator = Paginator(contents, 10)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)
    return render(request, 'land/article.html', {'content_list': page_obj, 'search_name': username, "name_length": contents.count()})



def NewSearchCountryContent(request, country):
    country_val = country.split(" ")[0]
    city_val = country.split(" ")[1]
    country_val_filter = Country.objects.filter(name__exact=country_val)
    city_val_filter = City.objects.filter(name_ascii__exact=city_val)
    if country_val_filter.exists() and city_val_filter.exists():
        
        country_val_id = Country.objects.get(name__exact=country_val)
        city_val_id = City.objects.get(name__exact=city_val)
        contents = Content.objects.filter(country_id=country_val_id.pk, city_id=city_val_id.pk, approved=True)
        paginator = Paginator(contents, 10)
        page = request.GET.get('page')
        page_obj = paginator.get_page(page)

        return render(request, 'land/article.html', {'content_list': page_obj, 'search_country': country, "country_length": contents.count()})
    else:
        empty_temp = []
        return render(request, 'land/article.html', {'content_list': empty_temp, 'search_country': country, "country_length": 0})

def check_credit(request):
    my_id = request.POST.get('value')
    review = ContentView.objects.filter(content_id=my_id, user_id=request.user.id)
    if review.exists():
        return HttpResponse('OK')
    else:
        user = User.objects.get(id=request.user.id)
        if user.credit != None:
            if int(user.credit) > 0:
                user.credit = int(user.credit) - 1
                user.save()
                review_c = ContentView(
                    view=True,
                    user_id=request.user.id,
                    content_id=my_id
                )
                review_c.save()
                return HttpResponse('OK')
            else:
                return HttpResponse('NO')
        else:
            return HttpResponse('NO')


def check_credit_article(request):
    my_id = request.POST.get('value')
    user = User.objects.get(id=my_id)
    if user.credit != None:
        if int(user.credit) > 0:
            user.credit = int(user.credit) - 1
            user.save()
            return HttpResponse('OK')
        else:
            return HttpResponse('NO')
    else:
        return HttpResponse('NO')

def create_commit(request):
    commit = request.POST.get('commit')
    articleid = request.POST.get('article')
    userid = request.POST.get('user')

    commit = Commit(
        commit = commit,
        user_id = userid,
        content_id = articleid
    )
    commit.save()
    return HttpResponse('OK')



       

