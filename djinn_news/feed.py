from django.utils.safestring import mark_safe
from djinn_contenttypes.base_feed import DjinnFeed
from djinn_contenttypes.models.feed import MoreInfoFeedGenerator
from djinn_news.views.newsviewlet import NewsViewlet
from pgprofile.models import GroupProfile
from django.utils.translation import gettext_lazy as _


class LatestNewsFeed(DjinnFeed):
    '''
    http://192.168.1.6xx:8000/news/latest/feed/
    '''
    title_prefix = _("Gronet:")
    title = _(f"{title_prefix} laatste nieuws")
    link = "/news/latest/feed/"
    description = _("Homepage laatste nieuws")
    feed_type = MoreInfoFeedGenerator

    parentusergroup_id = None

    def get_object(self, request, *args, **kwargs):

        groupprofile_id = kwargs.get('groupprofile_id', None)

        if groupprofile_id:
            groupprofile = GroupProfile.objects.get(id=groupprofile_id)
            self.title = _(f"{self.title_prefix} nieuws van "
                           f"'{groupprofile.title}'")
            self.description = _(f"{self.title_prefix} laatste "
                                 f"nieuwsartikelen in {groupprofile.title}")
            self.parentusergroup_id = groupprofile.usergroup_id

        return super().get_object(request, *args, **kwargs)

    def items(self):
        # re-use the news viewlet as it is on the homepage.
        newsviewlet = NewsViewlet()
        newsviewlet.kwargs = {
            'parentusergroup': self.parentusergroup_id,
            'limit_override': 100,
            'for_rssfeed': True,
            'items_no_image': self.items_no_image,
            'items_with_image': self.items_with_image,
        }

        newslist = newsviewlet.news()
        return newslist[:6]

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
        background_img_url = ""
        if item.content_object.has_feedimg:
            background_img_url = "%s%s" % (
                self.http_host, item.content_object.feed_bg_img_url)

        return {
            "background_img_url": background_img_url,
            "more_info_class": item.content_object.more_info_class,
            "more_info_text": item.content_object.more_info_text,
            "more_info_qrcode_url": item.content_object.qrcode_img_url(
                http_host=self.http_host)
        }