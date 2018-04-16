from django.apps import AppConfig
from django.db.models import signals


class DjinnNewsAppConfig(AppConfig):

    name = 'djinn_news'

    def ready(self):

        from djinn_news.management import create_permissions, register_events
        signals.post_migrate.connect(create_permissions, sender=self)
        signals.post_migrate.connect(register_events, sender=self)
        # signals.post_migrate.connect(set_default_settings, sender=self)
