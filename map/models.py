from djgeojson.fields import PolygonField, PointField
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_quest = models.IntegerField(default="1")
    second_quest = models.IntegerField(default="1")
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