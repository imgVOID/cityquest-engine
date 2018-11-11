from djgeojson.fields import PolygonField, PointField
from django.db import models


class MushroomSpot(models.Model):

    title = models.CharField(max_length=256)
    num = models.IntegerField(default="0")
    description = models.TextField()
    picture = models.CharField(max_length=100, default="")
    color = models.CharField(max_length=20, default="#ff7800")
    geom = PolygonField()
    def __str__(self):
        return self.title

    @property
    def picture_url(self):
        return self.picture.url

class Point(models.Model):

    title = models.CharField(max_length=256)
    num = models.IntegerField(default="0")
    description = models.TextField()
    picture = models.ImageField(blank=True)
    icon = models.TextField(default="")
    geom = PointField()

    def __str__(self):
        return self.title

    @property
    def picture_url(self):
        return self.picture.url
