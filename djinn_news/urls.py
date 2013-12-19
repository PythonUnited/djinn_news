from django.conf.urls.defaults import patterns, include, url
from models.news import News
from views.newsviewlet import NewsViewlet
from djinn_contenttypes.views.utils import generate_model_urls


_urlpatterns = patterns(
    "",

    url(r"^$",
        NewsViewlet.as_view(),
        name="djinn_news"),
    )

urlpatterns = patterns(
    '',
    (r'^news/', include(_urlpatterns)),
    (r'^news/', include(generate_model_urls(News))),
    )
