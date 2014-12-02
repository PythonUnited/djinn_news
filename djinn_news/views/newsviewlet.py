from django.views.generic import TemplateView
from django.conf import settings
from djinn_contenttypes.views.base import AcceptMixin
from djinn_contenttypes.models.highlight import Highlight
from djinn_news.models.news import News
from datetime import datetime
from django.db.models.query import Q


SHOW_N = getattr(settings, "DJINN_SHOW_N_NEWS_ITEMS", 5)


class NewsViewlet(AcceptMixin, TemplateView):

    template_name = "djinn_news/snippets/news_viewlet.html"

    def news(self, limit=SHOW_N):

        now = datetime.now()

        news_ids = Highlight.objects.filter(
            object_ct__name="news"
        ).filter(
            Q(date_from__isnull=True) | Q(date_from__lte=now)
        ).filter(
            Q(date_to__isnull=True) | Q(date_to__gte=now)
        ).values_list("object_id", flat=True)

        return News.objects.filter(
            id__in=news_ids
        ).filter(
            Q(publish_from__isnull=True) | Q(publish_from__lte=now)
        ).filter(
            Q(publish_to__isnull=True) | Q(publish_to__gte=now)
        ).exclude(title="").order_by('-publish_from', '-changed')[:limit]

    @property
    def show_more(self, limit=SHOW_N):

        return self.news(limit=None).count() > limit
