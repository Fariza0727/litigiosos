from django.conf.urls import url
from .views import LandPage, ArticleList, autocompleteModelSearch, NewSearchContent, autocompleteModelSearchCountry, NewSearchCountryContent, ArticleDetail, check_credit, create_commit, check_credit_article, TerminosYCondiciones

urlpatterns = [
               url(r'^$', LandPage.as_view(), name='land'),
               url(r'^article_list$', ArticleList.as_view(), name='article_list'),
               url(r'^terminosycondiciones$', TerminosYCondiciones.as_view(), name='tic_view'),
               url(r'^ajax_calls/search/', autocompleteModelSearch),
               url(r'^ajax_calls/searchcountry/', autocompleteModelSearchCountry),
               url(r'^article/(?P<username>[^/]+)/$', NewSearchContent, name='NewSearchContent'),
               url(r'^article/country/(?P<country>[^/]+)/$', NewSearchCountryContent, name='NewSearchCountryContent'),
               url(r'^article-detail/(?P<pk>[0-9]+)/$', ArticleDetail.as_view(), name='article_detail'),
               url(r'^check_credit/$', check_credit, name='check_credit'),
               url(r'^check_credit_article/$', check_credit_article, name='check_credit_article'),
               url(r'^create_commit/$', create_commit, name='create_commit'),
              ]