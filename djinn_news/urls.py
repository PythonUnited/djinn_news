from django.conf.urls import patterns, include, url
from models.news import News
from views.newsviewlet import NewsViewlet
from djinn_contenttypes.views.base import CreateView
from djinn_contenttypes.views.utils import generate_model_urls, find_form_class


news_form = find_form_class(News, "djinn_news")


_urlpatterns = patterns(
    "",

    url(r"^$",
        NewsViewlet.as_view(),
        name="djinn_news"),

    url(r"^add/news/(?P<parentusergroup>[\d]*)/$",
        CreateView.as_view(model=News, form_class=news_form,
                           fk_fields=["parentusergroup"]),
        name="djinn_news_add_news"),
    )

urlpatterns = patterns(
    '',
    (r'^news/', include(_urlpatterns)),
    (r'^news/', include(generate_model_urls(News))),
    )
