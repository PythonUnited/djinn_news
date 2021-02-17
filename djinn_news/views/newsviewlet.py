from django.views.generic import TemplateView
from django.conf import settings
from djinn_contenttypes.views.base import AcceptMixin, FeedViewMixin
from djinn_contenttypes.models.highlight import Highlight
from datetime import datetime
from django.db.models.query import Q

from djinn_news.models import News
from djinn_workflow.utils import get_state
from pgprofile.models import GroupProfile

SHOW_N = getattr(settings, "DJINN_SHOW_N_NEWS_ITEMS", 5)


class NewsWrapper(object):

    content_object = None

    def __init__(self, obj):
        self.content_object = obj


class NewsViewlet(AcceptMixin, FeedViewMixin, TemplateView):

    template_name = "djinn_news/snippets/news_viewlet.html"

    news_list = None
    has_more = False
    sticky_item = None
    limit = SHOW_N

    def parentusergroup(self):

        return self.kwargs.get('parentusergroup', None)

    def groupprofile(self):

        pugid = self.parentusergroup()
        if pugid:
            return GroupProfile.objects.filter(usergroup__id=pugid).last()
        return None

    @staticmethod
    def _news_published_filter(queryset, now):
        return queryset.filter(
            is_tmp=False
        ).filter(
            Q(publish_from__isnull=True) | Q(publish_from__lte=now)
        ).filter(
            Q(publish_to__isnull=True) | Q(publish_to__gte=now)
        ).order_by("-created")

    @staticmethod
    def _highlights_published(now):
        return Highlight.objects.filter(
            object_ct__model="news"
        ).filter(
            Q(date_from__isnull=True) | Q(date_from__lte=now)
        ).filter(
            Q(date_to__isnull=True) | Q(date_to__gte=now)
        ).order_by("-date_from")

    def get_queryset(self, queryset):
        queryset = super().get_queryset(queryset)

        if self.kwargs.get('items_with_image', False):
            queryset = queryset.filter(home_image__isnull=False)
        if self.kwargs.get('items_no_image', False):
            queryset = queryset.filter(home_image__isnull=True)

        return queryset

    def news(self):

        if self.parentusergroup():
            self.limit = 3

        limit_override = self.kwargs.get('limit_override', None)
        if limit_override:
            self.limit = limit_override

        now = datetime.now()

        if not self.news_list:

            # For Homepage, the news-items must be 'highlighted'.
            # In group, the newsitems may be returned directly
            pug = self.parentusergroup()
            if pug:
                pug = int(pug)

                highlighted = []

                news_qs = self.get_queryset(
                    News.objects.filter(parentusergroup_id=pug))

                # first max 'limit' sticky items
                for stickyitem in NewsViewlet._news_published_filter(
                        news_qs, now).filter(is_sticky=True):
                    highlighted.append(NewsWrapper(stickyitem))
                    if len(highlighted) >= self.limit:
                        break

                # then, not stick
                for newsitem in NewsViewlet._news_published_filter(
                        news_qs, now).filter(is_sticky=False):
                    highlighted.append(NewsWrapper(newsitem))
                    if len(highlighted) >= 2*self.limit:
                        break
            else:

                sticky_ids = NewsViewlet._news_published_filter(
                    News.objects.all(), now).filter(
                    is_sticky=True).values_list("id")

                highlighted_sticky = NewsViewlet._highlights_published(now).filter(
                    object_id__in=sticky_ids
                )
                highlighted_not_sticky = NewsViewlet._highlights_published(now).exclude(
                    object_id__in=sticky_ids
                )
                highlighted = []
                # bit nasty, but we do not want a list like this: [None]
                first_highligted = highlighted_sticky.first()
                if first_highligted:
                    highlighted.append(first_highligted)

                [highlighted.append(not_sticky) for not_sticky in
                 highlighted_not_sticky[:self.limit+1]]


            self.news_list = []

            evaluated_item_count = 0
            for hl in highlighted:
                evaluated_item_count += 1

                news = hl.content_object
                if news.is_tmp:
                    continue

                state = get_state(news)
                if news:
                    if state.name == "private":
                        continue
                    if self.kwargs.get('items_with_image', False) and not news.home_image:
                        continue
                    if self.kwargs.get('items_no_image', False) and news.home_image:
                        continue

                    if self.for_rssfeed and not news.publish_for_feed:
                        # skip looking for rss items after 100 highights
                        if evaluated_item_count < 100:
                            # highlighted news items die niet rss-feed enabled zijn
                            # sowieso niet opnemen in de lijst.
                            continue

                    if (not news.publish_from or news.publish_from <= now) and \
                            (not news.publish_to or news.publish_to > now) and \
                            news.title:

                        if news.is_sticky and not self.sticky_item and not pug:
                            # sticky item presentation (large picture) only on homepage
                            self.sticky_item = news
                            if self.for_rssfeed and news.publish_for_feed:
                                self.news_list.append(hl)
                        else:
                            if not self.for_rssfeed or news.publish_for_feed:
                                self.news_list.append(hl)

                if len(self.news_list) >= self.limit:
                    self.has_more = True
                    if self.sticky_item:
                        # keep going if we don't have a sticky item yet.
                        # if we are unfortunate, we need to loop over all.
                        break
        return self.news_list[:self.limit]


    @property
    def show_more(self):
        if not self.news_list:
            self.news()
        return self.has_more
