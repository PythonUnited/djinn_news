from django.conf.urls.defaults import patterns, include
from models.news import News
from djinn_contenttypes.views.utils import generate_model_urls


_urlpatterns = patterns(
    "",
    )

urlpatterns = patterns(
    '',
    (r'^news/', include(_urlpatterns)),
    (r'^news/', include(generate_model_urls(News))),
    )
