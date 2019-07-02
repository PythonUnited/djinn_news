from django.conf.urls import url
from django.urls import include, path

from djinn_news.feed import LatestNewsFeed
from .models.news import News
from .views.newsviewlet import NewsViewlet
from djinn_contenttypes.views.base import CreateView
from djinn_contenttypes.views.utils import generate_model_urls, find_form_class


news_form = find_form_class(News, "djinn_news")


_urlpatterns = [

    url(r"^$",
        NewsViewlet.as_view(),
        name="djinn_news"),

    url(r"^(?P<parentusergroup>[\d]*)/?$",
        NewsViewlet.as_view(),
        name="djinn_news_pug"),

    url(r"^add/news/(?P<parentusergroup>[\d]*)/$",
        CreateView.as_view(model=News, form_class=news_form,
                           fk_fields=["parentusergroup"]),
        name="djinn_news_add_news"),

    # homepage nieuws-feed voor narrowcasting
    path('latest/feed/', LatestNewsFeed()),

    # groepspagina nieuws-feed voor narrowcasting
    # het groupprofile_id kan gevonden worden door in een groepspagina
    # boven de link naar 'Bekijk de content in deze groep' te bekijken
    path('latest/feed/group/<int:groupprofile_id>/', LatestNewsFeed()),
]

urlpatterns = [
    url(r'^news/', include(_urlpatterns)),
    url(r'^news/', include(generate_model_urls(News))),
]
