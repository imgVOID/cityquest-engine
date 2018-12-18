from django.contrib.auth.admin import UserAdmin
from leaflet.admin import LeafletGeoAdmin
from django.contrib import admin
from guardian.admin import GuardedModelAdmin

from . import models as models

class PolygonInline(admin.StackedInline):
    model = models.Polygon
    ordering = ("level",)
    extra = 0
    show_change_link = True
    
class MarkerInline(admin.StackedInline):
    model = models.Marker
    ordering = ("level",)
    extra = 0
    show_change_link = True


class QuestAdmin(LeafletGeoAdmin):
    inlines = [PolygonInline,MarkerInline]
    
class PolygonAdmin(LeafletGeoAdmin):
    search_fields = ('quest__id','quest__title')
    
class MarkerAdmin(LeafletGeoAdmin):
    search_fields = ('quest__id','quest__title')

admin.site.register(models.Profile, admin.ModelAdmin)
admin.site.register(models.Quest, QuestAdmin)
admin.site.register(models.Polygon, PolygonAdmin)
admin.site.register(models.Marker, MarkerAdmin)
admin.site.register(models.FirstQuestPolygon, admin.ModelAdmin)
admin.site.register(models.FirstQuestMarker, admin.ModelAdmin)
admin.site.register(models.SecondQuestPolygon, admin.ModelAdmin)
admin.site.register(models.SecondQuestMarker, admin.ModelAdmin)
