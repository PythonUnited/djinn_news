from django.contrib.syndication.views import Feed
from django.urls import reverse
from django.utils import feedgenerator
from django.utils.feedgenerator import Enclosure
from django.utils.safestring import mark_safe

from djinn_news.views.newsviewlet import NewsViewlet
from pgcontent.templatetags.contentblock_tags import fetch_image_url
from pgprofile.models import GroupProfile


class LatestNewsFeed(Feed):
    '''
    http://192.168.1.6:8000/news/latest/feed/
    '''
    title_prefix = "Gronet:"
    title = "%s laatste nieuws" % title_prefix
    link = "/news/latest/feed/"
    description = "Homepage laatste nieuws"
    feed_type = feedgenerator.DefaultFeed

    parentusergroup_id = None

    def get_object(self, request, *args, **kwargs):

        self.http_host = "%s://%s" % (
            request.scheme, request.META.get('HTTP_HOST', 'localhost:8000'))

        groupprofile_id = kwargs.get('groupprofile_id', None)

        if groupprofile_id:
            groupprofile = GroupProfile.objects.get(id=groupprofile_id)
            self.title = "%s nieuws van '%s'" % (
                self.title_prefix, groupprofile.title)
            self.description = "%s laatste nieuwsartikelen in %s" % (
                self.title_prefix, groupprofile.title)
            self.parentusergroup_id = groupprofile.usergroup_id

        return super().get_object(request, *args, **kwargs)

    def items(self):
        # re-use the news viewlet as it is on the homepage.
        newsviewlet = NewsViewlet()
        newsviewlet.kwargs = {
            'parentusergroup': self.parentusergroup_id,
            'limit_override': 6,
            'for_rssfeed': True
        }

        newslist = newsviewlet.news()
        return newslist

    def item_title(self, item):

        return item.content_object.title

    def item_description(self, item):
        img_url = fetch_image_url(item.content_object.home_image,
                              'news_feed_default', 'news')
        img_url = "%s%s" % (self.http_host, img_url)
        # print(img_url)
        desc = '<img src="%s" />' % img_url

        desc += '<div>%s</div>' % item.content_object.description_feed

        return mark_safe(desc)

    # item_link is only needed if NewsItem has no get_absolute_url method.
    def item_link(self, item):
        # TODO: nadenken over detail pagina die niet achter inlog zit?
        # return reverse('djinn_news_view_news', args=[
        #     item.content_object.pk, item.content_object.slug])
        return "/"

    # Dit hebben we hoogstwaarschijnlijk niet nodig.
    # Nog even laten staan vanwege het uitzoekwerk .... :-)
    #
    # def item_enclosures(self, item):
    #
    #     img_url = fetch_image_url(item.content_object.home_image,
    #                           'news_feed_default', 'news')
    #
    #     img_url = "http://192.168.1.6:8000%s" % img_url
    #
    #     if item.content_object.home_image:
    #         mimetype = 'image/%s' % item.content_object.home_image.image.name.split('.')[-1]
    #         length = str(item.content_object.home_image.image.size)
    #     else:
    #         mimetype = 'image/%s' % img_url.split('.')[-1]
    #         length='10000'
    #
    #     encl = Enclosure(img_url, length=length, mime_type=mimetype)
    #
    #     return [encl]