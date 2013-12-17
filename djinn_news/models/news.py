from django.db import models
from django.utils.translation import ugettext_lazy as _
from djinn_contenttypes.registry import CTRegistry
from djinn_contenttypes.models.publishable import PublishableContent
from djinn_contenttypes.models.attachment import ImgAttachment


class News(PublishableContent):

    """ News content type """

    text = models.TextField(null=True, blank=True)

    images = models.ManyToManyField(ImgAttachment)

    show_images = models.BooleanField(default=True)

    is_global = models.BooleanField(default=False)

    comments_enabled = models.BooleanField(default=True)

    @property
    def documents(self):

        return self.get_related(relation_type="related_document")

    class Meta:
        app_label = "djinn_news"


CTRegistry.register(
    "news",
    {"class": News,
     "app": "djinn_news",
     "label": _("News")}
    )
