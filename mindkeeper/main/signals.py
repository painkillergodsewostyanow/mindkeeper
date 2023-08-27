from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Themes, Cards


@receiver(post_save, sender=Themes)
def update_themes_search_vector(sender, instance, created, update_fields, **kwargs):
    instance.update_search_vector('title')


@receiver(post_save, sender=Cards)
def update_cards_search_vector(sender, instance, created, update_fields, **kwargs):
    instance.update_search_vector('title', 'content')
