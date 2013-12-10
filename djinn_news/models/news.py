from django.db import models
from django.utils.translation import ugettext_lazy as _
from djinn_contenttypes.registry import CTRegistry
from djinn_contenttypes.models.publishable import PublishableContent


class News(PublishableContent):

    """ News content type """

    body = models.TextField(null=True, blank=True)

    #documents = models.ManyToManyField(DocumentAttachment, null=True,
    #                                   blank=True)
    #images = models.ManyToManyField(ImageAttachment, null=True, blank=True)

    show_carousel = models.BooleanField(default=True)

    class Meta:
        app_label = "djinn_news"


CTRegistry.register(
    "djinn_news.news",
    {"class": News,
     "app": "djinn_news",
     "label": _("News")}
    )
