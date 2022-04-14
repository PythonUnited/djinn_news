from django.db.models.functions import Coalesce
from django.views.generic import TemplateView
from django.conf import settings
from djinn_contenttypes.views.base import AcceptMixin, FeedViewMixin, \
    DesignVersionMixin
from djinn_contenttypes.models.highlight import Highlight
from datetime import datetime
from django.db.models.query import Q
from djinn_news.models import News
from djinn_workflow.models import ObjectState
from pgprofile.models import GroupProfile

SHOW_N = getattr(settings, "DJINN_SHOW_N_NEWS_ITEMS", 5)


class NewsWrapper(object):

    content_object = None

    def __init__(self, obj):
        self.content_object = obj


class NewsViewlet(DesignVersionMixin, AcceptMixin, FeedViewMixin, TemplateView):

    template_name = "djinn_news/snippets/news_viewlet.html"

    news_list = None
    has_more = False
    sticky_item = None
    limit = SHOW_N
    categories_title = None

    @property
    def parentusergroup_id(self):

        pugid = self.kwargs.get('parentusergroup', None)
        if pugid:
            return int(pugid)
        return None

    def groupprofile(self):

        pugid = self.parentusergroup_id
        if pugid:
            return GroupProfile.objects.filter(usergroup__id=pugid).last()
        return None

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['categories_title'] = self.request.GET.get('title', 'Nieuws')
        return ctx

    def get_queryset(self, queryset):
        queryset = super().get_queryset(queryset)

        if self.kwargs.get('items_with_image', False):
            queryset = queryset.filter(home_image__isnull=False)
        if self.kwargs.get('items_no_image', False):
            queryset = queryset.filter(home_image__isnull=True)

        # als er om een specifieke categorie wordt gevraagd
        if self.category_slugs:
            queryset = queryset.filter(category__slug__in=self.category_slugs)

        if self.category_slugs_excluded:
            queryset = queryset.exclude(category__slug__in=self.category_slugs_excluded)

        queryset = queryset.exclude(
            id__in=ObjectState.objects.filter(
                object_ct__model='news',
                state__name='private'
            ).values_list('object_id', flat=True)
        )

        return queryset

    @staticmethod
    def _news_published_filter(queryset, now):
        return queryset.filter(
            is_tmp=False
        ).filter(
            Q(publish_from__isnull=True) | Q(publish_from__lte=now)
        ).filter(
            Q(publish_to__isnull=True) | Q(publish_to__gte=now)
        # ).order_by("-publish_from", "-created")
        # Sortering moet obv published_from, maar die is leeg als het artikel
        # niet op de Homepage staat of heeft gestaan.
        # Daarom wordt in de DB-query de combinatie (Coalesce) van published_from
        # en created gemaakt en daarmee de eerste 'gevulde' waarde gebruikt.
        ).annotate(
            sort_datetime=Coalesce('publish_from', 'created')
        ).order_by('-sort_datetime')

    @staticmethod
    def _highlights_published(now):
        # alleen voor Homepage news
        return Highlight.objects.filter(
            object_ct__model="news"
        ).filter(
            Q(date_from__isnull=True) | Q(date_from__lte=now)
        ).filter(
            Q(date_to__isnull=True) | Q(date_to__gte=now)
        ).order_by("-date_from")


    def news(self):

        self.categories_title = self.request.GET.get('title', 'Nieuws')
        self.category_slugs = self.request.GET.get('categories', False)
        if self.category_slugs:
            self.categories = self.category_slugs
            self.category_slugs = self.category_slugs.split(',')
        self.category_slugs_excluded = self.request.GET.get('skip', False)
        if self.category_slugs_excluded:
            self.category_slugs_excluded = self.category_slugs_excluded.split(',')

        self.offset = int(self.request.GET.get('offset', 0))

        pugid = self.parentusergroup_id
        if pugid:
            self.limit = 3

        limit_override = self.kwargs.get('limit_override', None)
        if limit_override:
            self.limit = limit_override

        now = datetime.now()

        # cheap ass caching
        if self.news_list:
            return self.news_list

        self.news_list = []

        # For Homepage, the news-items must be 'highlighted'.
        # In group, the newsitems may be returned directly
        if pugid:
            # news in Group
            news_qs = self.get_queryset(
                News.objects.filter(parentusergroup_id=pugid))

            # # first max 'limit' sticky items
            # for stickynews in NewsViewlet._news_published_filter(
            #         news_qs, now).filter(is_sticky=True):
            #     self.news_list.append(stickynews)
            #     if len(self.news_list) >= self.limit:
            #         break

            # then, not stick
            news_qs = NewsViewlet._news_published_filter(news_qs, now)

            #men wil geen autoaanvulling op de homepage
            #self.has_more = news_qs.count() > self.limit

            for newsitem in news_qs[self.offset:self.offset+self.limit]:
                self.news_list.append(newsitem)

        else:
            # news on HomePage
            # 1. haal alle news-Highlights op
            highlighted_news_ids = NewsViewlet._highlights_published(now).values_list('object_id', flat=True)

            # 2. haal alle News items op, max 1 sticky item eerst
            self.sticky_item = NewsViewlet._news_published_filter(
                self.get_queryset(News.objects.filter(is_sticky=True, id__in=highlighted_news_ids)),
                now
            ).first()
            # if self.sticky_item:
            #     self.news_list.append(self.sticky_item)

            news_qs = NewsViewlet._news_published_filter(
                self.get_queryset(News.objects.filter(id__in=highlighted_news_ids)),
                now
            )
            if self.sticky_item:
                # don't show this one twice
                news_qs = news_qs.exclude(id=self.sticky_item.id)

            if self.offset:
                # alleen bij de 'eerste call' het sticky news item tonen, daarna niet meer
                # Hierboven wel nodig om hem uit de resultset te halen...
                self.sticky_item = None

            # de items die gehighlight zijn voor de homepage EN gepubliceerd staan
            published_news_ids = news_qs.values_list("id", flat=True)
            published_highlighted_news_ids = []
            # de volgorde van van publiceren zit in highlighted_news_ids
            # Die willen we aanhouden, maar de niet-gepubliceerden eruit gooien
            for highlighted_news_id in highlighted_news_ids:
                if highlighted_news_id in published_news_ids:
                    published_highlighted_news_ids.append(highlighted_news_id)

            # En nu de instances erbij halen.
            for sorted_published_hightlight_id in published_highlighted_news_ids[
                                                  self.offset:self.offset+self.limit]:
                self.news_list.append(News.objects.get(id=sorted_published_hightlight_id))

            # oude constructie voor ophalen/sorteren. Met bug erin...
            # #men wil geen autoaanvulling op de homepage
            # #self.has_more = news_qs.count() > self.offset + self.limit
            # unsorted_news_dict = {}
            # for news_item in news_qs[self.offset:self.offset+self.limit]:
            #     unsorted_news_dict[news_item.id] = news_item
            #     # self.news_list.append(news_item)
            #
            # # sorteren op volgorde van Highlights
            # for news_item_id in highlighted_news_ids:
            #     sorted_news_item = unsorted_news_dict.get(news_item_id, False)
            #     if sorted_news_item:
            #         self.news_list.append(sorted_news_item)

        self.next_offset = self.offset + len(self.news_list)

        return self.news_list

    @property
    def show_more(self):
        if not self.news_list:
            self.news()
        return self.has_more
