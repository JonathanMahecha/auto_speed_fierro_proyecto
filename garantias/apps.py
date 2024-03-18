from django.apps import AppConfig


class GarantiasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'garantias'

class GarantiasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'garantias'

    def ready(self):
        import garantias.signals 