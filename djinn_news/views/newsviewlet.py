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
                news_qs = self.get_queryset(News.objects.all())

                for newsitem in news_qs.filter(
                    parentusergroup_id=pug
                ).filter(
                    Q(publish_from__isnull=True) | Q(publish_from__lte=now)
                ).filter(
                    Q(publish_to__isnull=True) | Q(publish_to__gte=now)
                ).order_by("-created"):
                    highlighted.append(NewsWrapper(newsitem))
            else:
                highlighted = Highlight.objects.filter(
                    object_ct__model="news"
                ).filter(
                    Q(date_from__isnull=True) | Q(date_from__lte=now)
                ).filter(
                    Q(date_to__isnull=True) | Q(date_to__gte=now)
                ).order_by("-date_from")

            self.news_list = []

            evaluated_item_count = 0
            for hl in highlighted:
                evaluated_item_count += 1

                news = hl.content_object

                # if news.parentusergroup_id != pug:
                    # Only group-news in group-viewlet
                    # only newsitems without parentusergroup on homepageviewlet
                #    continue

                state = get_state(news)
                if news and state.name == "private":
                    continue
                if self.for_rssfeed and news and not news.publish_for_feed:
                    # skip looking for rss items after 100 highights
                    if evaluated_item_count > 100:
                        break
                    # highlighted news items die niet rss-feed enabled zijn
                    # sowieso niet opnemen in de lijst.
                    continue

                if news and (not news.publish_from or news.publish_from <= now) and \
                        (not news.publish_to or news.publish_to > now) and \
                        news.title:

                    if news.is_sticky and not self.sticky_item and not pug:
                        # sticky item presentation (large picture) only on homepage
                        self.sticky_item = news
                        if self.for_rssfeed:
                            self.news_list.append(hl)
                    else:
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
