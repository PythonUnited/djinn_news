from django.utils.safestring import mark_safe
from djinn_contenttypes.base_feed import DjinnFeed
from djinn_contenttypes.models.feed import MoreInfoFeedGenerator
from djinn_contenttypes.settings import FEED_HEADER_NORMAL_SIZE
from djinn_news.views.newsviewlet import NewsViewlet
from pgcontent.templatetags.contentblock_tags import fetch_image_url
from pgprofile.models import GroupProfile
from image_cropping.utils import get_backend


class LatestNewsFeed(DjinnFeed):
    '''
    http://192.168.1.6xx:8000/news/latest/feed/
    '''
    title_prefix = "Gronet:"
    title = "%s laatste nieuws" % title_prefix
    link = "/news/latest/feed/"
    description = "Homepage laatste nieuws"
    feed_type = MoreInfoFeedGenerator

    parentusergroup_id = None

    def get_object(self, request, *args, **kwargs):

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

        desc = '<div>%s</div>' % item.content_object.description_feed

        return mark_safe(desc)


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

    def item_extra_kwargs(self, item):
        info_text = None
        if len(item.content_object.keywordslist) > 0:
            info_text = "Zoek op: " + " + ".join(
                item.content_object.keywordslist)

        content_url = "%s%s" % (
                self.http_host, item.content_object.get_absolute_url())

        qrcode_img_url = self.get_qrcode_img_url(content_url, item.content_object)

        background_img_url = None,
        if item.content_object.home_image:
            background_img_url = get_backend().get_thumbnail_url(
                item.content_object.home_image.image,
                {
                    'size': FEED_HEADER_NORMAL_SIZE,
                    'box': item.content_object.home_image_feed_crop,
                    'crop': True,
                    'detail': True,
                }
            )

        return {
            "background_img_url": "%s%s" % (self.http_host, background_img_url),
            "more_info_class": "gronet",
            "more_info_text": info_text,
            "more_info_qrcode_url": qrcode_img_url
        }