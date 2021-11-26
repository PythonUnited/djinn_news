from datetime import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _
from djinn_contenttypes.models.category import CategoryMixin
from image_cropping import ImageRatioField

from djinn_contenttypes.models.feed import FeedMixin
from djinn_contenttypes.registry import CTRegistry
from djinn_contenttypes.models.publishable import PublishableContent
from djinn_contenttypes.models.attachment import ImgAttachment
from djinn_contenttypes.models.commentable import Commentable
from djinn_contenttypes.models.highlight import Highlight
from djinn_contenttypes.settings import FEED_HEADER_SIZE
from djinn_likes.models.likeable import LikeableMixin


class News(PublishableContent, Commentable, LikeableMixin, FeedMixin, CategoryMixin):

    """ News content type """
    # BEGIN required by FeedMixin
    feed_bg_img_fieldname = 'image_feed'
    feed_bg_img_crop_fieldname = 'image_feed_crop'
    # END required by FeedMixin


    text = models.TextField(null=True, blank=True)

    images = models.ManyToManyField(ImgAttachment)

    home_image = models.ForeignKey(ImgAttachment,
                                   related_name='news_home_image',
                                   null=True, blank=True,
                                   on_delete=models.SET_NULL)

    image_feed = models.ForeignKey(
        ImgAttachment,
        related_name='news_image',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        help_text=_("Image for the rss-feed. Minimal width is 1920px, minimal heigt 500px.")
    )

    image_feed_crop = ImageRatioField(
        'image_feed__image', "%sx%s" % (
            FEED_HEADER_SIZE['news'][0], FEED_HEADER_SIZE['news'][1]),
        help_text=_("Part of the image_feed to use in the rss-feed. Upload or "
                    "change home_image, click 'save and edit again' and then "
                    "you can select a region to use in the rss feed."),
        verbose_name = _("Foto uitsnede")
    )

    show_images = models.BooleanField(default=True)

    is_global = models.BooleanField(default=False)

    is_sticky = models.BooleanField(default=False)

    create_tmp_object = True

    def documents(self):

        return self.get_related(relation_type="related_document")

    @property
    def date(self):

        return self.publish_from or self.created

    @property
    def human_date(self):

        delta = datetime.now() - self.date

        if delta.days == 0:
            return self.date.strftime('%H:%M')
        else:
            return self.date.strftime('%d-%m')

    @property
    def highlight_from(self):

        try:
            return Highlight.objects.get(
                object_id=self.id,
                object_ct__model="news").date_from
        except:
            return None

    class Meta:
        app_label = "djinn_news"


CTRegistry.register(
    "news",
    {"class": News,
     "app": "djinn_news",
     "group_add": True,
     "allow_saveandedit": True,
     "label": _("News")}
    )
