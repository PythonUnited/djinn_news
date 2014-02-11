import logging
from datetime import datetime
from notification import models as notification
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from pgauth.models import UserGroup
from pgevents.events import Events
from news import News


LOGGER = logging.getLogger("djinn_news")
NEW_NEWS = "new_news"

@receiver(post_save, sender=News)
def post_save_news(sender, instance, **kwargs):

    if kwargs.get("created"):
        try:
            redaction = UserGroup.objects.get(name="webredactie")

            notification.send(
                redaction.members.all(),
                "request_news",
                {'object': instance}
                )
        except:
            LOGGER.exception("Couldn't send notification for news")


@receiver(pre_save, sender=News)
def news_pre_save(sender, instance, **kwargs):

    if instance.id and instance.title and instance.publish_from and \
            instance.publish_from <= datetime.now():
        # We do not create activities when title is empty

        context = {
            "content_item": instance,
            "title": instance.title,
            "url": instance.get_absolute_url(),
            "parentusergroup": instance.parentusergroup}

        if not instance.publish_notified:
            Events.send(
                NEW_NEWS,
                user=instance.changed_by,
                context=context,
                usergroup=instance.parentusergroup)
            instance.publish_notified = True
