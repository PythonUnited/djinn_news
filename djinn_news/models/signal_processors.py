import logging
from notification import models as notification
from django.db.models.signals import post_save
from django.dispatch import receiver
from pgauth.models import UserGroup
from pgevents.events import Events
from news import News


LOGGER = logging.getLogger("djinn_news")


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

        context = {
            "content_item": instance,
            "title": instance.title,
            "url": instance.get_absolute_url(),
            "parentusergroup": instance.parentusergroup}

        Events.send(
            "new_news",
            user=instance.changed_by,
            context=context,
            usergroup=instance.parentusergroup)