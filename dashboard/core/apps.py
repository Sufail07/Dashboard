from django.apps import AppConfig
from django.db.models.signals import post_migrate


class CoreConfig(AppConfig):
    name = 'core'

    def ready(self):
        from core.seed import seed_default_admin

        post_migrate.connect(seed_default_admin, sender=self)
