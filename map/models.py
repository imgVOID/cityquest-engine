from djgeojson.fields import PolygonField, PointField
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from django.core.cache import cache

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id1 = models.IntegerField(default="1")
    id2 = models.IntegerField(default="1")
    bio = models.TextField(max_length=500, blank=True)
    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Quest(models.Model):

    id = models.PositiveIntegerField(primary_key=True)
    title = models.CharField(max_length=256)
    description = models.TextField()
    def __str__(self):
        return self.title


class Polygon(models.Model):
    quest = models.ForeignKey(Quest, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    level = models.IntegerField(default="1")
    description = models.TextField()
    picture = models.CharField(max_length=100, default="")
    color = models.CharField(max_length=20, default="#ff7800")
    geom = PolygonField()

    def __str__(self):
        return self.title
    @property
    def picture_url(self):
        return self.picture
@receiver(post_save, sender=Polygon)
@receiver(post_delete, sender=Polygon)
def delete_polygons(instance, **kwargs):
    cache.delete('polygons')

class Marker(models.Model):
    quest = models.ForeignKey(Quest, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    level = models.IntegerField(default="1")
    description = models.TextField()
    picture = models.CharField(max_length=100, default="")
    icon = models.TextField(default="")
    geom = PointField()

    def __str__(self):
        return self.title
    @property
    def picture_url(self):
        return self.picture
@receiver(post_save, sender=Marker)
@receiver(post_delete, sender=Marker)
def delete_markers(instance, **kwargs):
    cache.delete('markers')

class FirstQuestPolygon(models.Model):

    title = models.CharField(max_length=256)
    level = models.IntegerField(default="1")
    description = models.TextField()
    picture = models.CharField(max_length=100, default="")
    color = models.CharField(max_length=20, default="#ff7800")
    geom = PolygonField()
    def __str__(self):
        return self.title
    @property
    def picture_url(self):
        return self.picture

class FirstQuestMarker(models.Model):
    title = models.CharField(max_length=256)
    level = models.IntegerField(default="1")
    description = models.TextField()
    picture = models.CharField(max_length=100, default="")
    icon = models.TextField(default="")
    geom = PointField()

    def __str__(self):
        return self.title
    @property
    def picture_url(self):
        return self.picture

class SecondQuestPolygon(models.Model):

    title = models.CharField(max_length=256)
    level = models.IntegerField(default="1")
    description = models.TextField()
    picture = models.CharField(max_length=100, default="")
    color = models.CharField(max_length=20, default="#ff7800")
    geom = PolygonField()
    def __str__(self):
        return self.title
    @property
    def picture_url(self):
        return self.picture

class SecondQuestMarker(models.Model):

    title = models.CharField(max_length=256)
    level = models.IntegerField(default="1")
    description = models.TextField()
    picture = models.CharField(max_length=100, default="")
    icon = models.TextField(default="")
    geom = PointField()

    def __str__(self):
        return self.title
    @property
    def picture_url(self):
        return self.picture