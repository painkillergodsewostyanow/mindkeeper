from django.apps import AppConfig


class SocietyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'society'

    def ready(self):
        from .signals import crop_user_image
