from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.urls import include, path

from djinn_news.feed import LatestNewsFeed
from .models import LiveBlog, LiveBlogUpdate
from .models.news import News
from .views.liveblogupdate import LiveBlogUpdateCreateView, \
    LiveBlogUpdateUpdateView, LiveBlogUpdateCountAjax, \
    LiveBlogUpdateLoadMoreAjax
from .views.liveblogviewlet import LiveBlogViewlet
from .views.newsviewlet import NewsViewlet
from djinn_contenttypes.views.base import CreateView, UpdateView, DetailView
from djinn_contenttypes.views.utils import generate_model_urls, find_form_class


news_form = find_form_class(News, "djinn_news")
liveblog_form = find_form_class(LiveBlog, "djinn_news")
liveblogupdate_form = find_form_class(LiveBlogUpdate, "djinn_news")

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


_urlpatterns_liveblog = [

    url(r"^$",
        login_required(LiveBlogViewlet.as_view()),
        name="djinn_news_liveblog"),

    url(r"^(?P<parentusergroup>[\d]*)/?$",
        login_required(LiveBlogViewlet.as_view()),
        name="djinn_news_liveblog_pug"),

    url(r"^add/liveblogupdate/(?P<liveblog>[\d]*)/$",
        login_required(LiveBlogUpdateCreateView.as_view(
            model=LiveBlogUpdate, form_class=liveblogupdate_form, fk_fields=["liveblog"])),
        name="djinn_news_add_liveblogupdate"),

    url(r"^edit/liveblogupdate/(?P<pk>[\d]*)/$",
        login_required(LiveBlogUpdateUpdateView.as_view(
            model=LiveBlogUpdate, form_class=liveblogupdate_form,)),
        name="djinn_news_edit_liveblogupdate"),

    url(r"^view/liveblogupdate/(?P<pk>[\d]*)/(?P<slug>[\-\d\w]+)/$",
        login_required(DetailView.as_view(
            model=LiveBlogUpdate)),
        name="djinn_news_view_liveblogupdate"),

    url(r"^add/(?P<parentusergroup>[\d]*)/$",
        login_required(CreateView.as_view(
            model=LiveBlog, form_class=liveblog_form,
            fk_fields=["parentusergroup"])),
        name="djinn_news_add_liveblog"),

    url(r"^view/liveblogupdatecount_ajax/(?P<pk>[\d]+)$",
        login_required(LiveBlogUpdateCountAjax.as_view(
            content_type='text/plain'
        )),
        name="djinn_news_liveblogupdatecount_ajax"),

    url(r"^view/liveblogupdateloadmore_ajax/(?P<pk>[\d]+)$",
        login_required(LiveBlogUpdateLoadMoreAjax.as_view(
            content_type='text/plain'
        )),
        name="djinn_news_liveblogupdateloadmore_ajax"),

]

urlpatterns = [
    url(r'^news/', include(_urlpatterns)),
    url(r'^news/live/', include(_urlpatterns_liveblog)),

    url(r'^news/', include(generate_model_urls(News))),
    url(r'^news/', include(generate_model_urls(LiveBlog))),
]
