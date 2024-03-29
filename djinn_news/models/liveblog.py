from datetime import datetime

from django.db import models
from django.db.models import Q
from image_cropping import ImageRatioField

from djinn_contenttypes.models import ImgAttachment
from djinn_contenttypes.models.commentable import Commentable
from djinn_contenttypes.models.feed import FeedMixin
from djinn_contenttypes.models.publishable import PublishableContent
from djinn_contenttypes.registry import CTRegistry
from djinn_contenttypes.settings import FEED_HEADER_SIZE
from djinn_likes.models.likeable import LikeableMixin
from django.utils.translation import gettext_lazy as _


class LiveBlog(PublishableContent, Commentable, LikeableMixin, FeedMixin):

    # BEGIN required by FeedMixin
    feed_bg_img_fieldname = 'image_feed'
    feed_bg_img_crop_fieldname = 'image_feed_crop'
    # END required by FeedMixin

    text = models.TextField(null=True, blank=True)

    home_image = models.ForeignKey(
        ImgAttachment,
        related_name='liveblog_home_image',
        null=True, blank=True,
        on_delete=models.SET_NULL)

    image_feed = models.ForeignKey(
        ImgAttachment,
        related_name='liveblog_image',
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

    @property
    def published_liveblogupdates(self):

        updates_qs = self.liveblogupdates.filter(is_tmp=False)

        updates_qs = updates_qs.filter(
            Q(publish_from__isnull=True)|Q(publish_from__lte=datetime.now())
        )

        return updates_qs

    class Meta:
        app_label = "djinn_news"

CTRegistry.register(
    "liveblog",
    {"class": LiveBlog,
     "app": "djinn_news",
     "group_add": True,
     "allow_saveandedit": True,
     "label": _("LiveBlog"),
     "name_plural": _('Liveblogs')
     }
)


class LiveBlogUpdate(PublishableContent, Commentable, LikeableMixin):

    liveblog = models.ForeignKey(
        LiveBlog,
        verbose_name=_('LiveBlog'),
        on_delete=models.CASCADE,
        related_name='liveblogupdates',
        help_text=_("The parent of this LiveBlog update")
    )

    text = models.TextField(null=True, blank=True)

    show_images = models.BooleanField(
        _("Afbeeldingen tonen"),
        default=True,
        help_text=_("Toon de afbeelding(en) onderaan deze update")
    )

    images = models.ManyToManyField(
        ImgAttachment,
        blank=True,
    )

    @property
    def permission_authority(self):
        # heb je permissies op de LiveBlog instance, dan ook op de
        # onderliggende LiveBlogUpdates
        return self.liveblog

    def save(self, *args, **kwargs):

        if self.liveblog:
            # The updates are always in the same parentusergroup
            self.parentusergroup_id = self.liveblog.parentusergroup_id

        return super().save(*args, **kwargs)

    class Meta:
        ordering = ["-created"]

CTRegistry.register(
    "liveblogupdate",
    {"class": LiveBlogUpdate,
     "app": "djinn_news",
     "group_add": True,
     "delete_permission": "djinn_news.delete_liveblogupdate",
     "allow_saveandedit": True,
     "label": _("LiveBlogUpdate")}
)
