from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Quest, Polygon, Marker

@receiver(post_save, sender=Quest)
@receiver(post_delete, sender=Quest)
def delete_quests(instance, **kwargs):
    cache.clear()

@receiver(post_save, sender=Polygon)
@receiver(post_delete, sender=Polygon)
def delete_polygons(instance, **kwargs):
    cache.clear()

@receiver(post_save, sender=Marker)
@receiver(post_delete, sender=Marker)
def delete_markers(instance, **kwargs):
    cache.clear()