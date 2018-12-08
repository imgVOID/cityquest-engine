from django.contrib.auth.admin import UserAdmin
from leaflet.admin import LeafletGeoAdmin
from django.contrib import admin
from guardian.admin import GuardedModelAdmin

from . import models as models


admin.site.register(models.Profile, admin.ModelAdmin)
admin.site.register(models.FirstQuestPolygon, admin.ModelAdmin)
admin.site.register(models.FirstQuestMarker, admin.ModelAdmin)
admin.site.register(models.SecondQuestPolygon, admin.ModelAdmin)
admin.site.register(models.SecondQuestMarker, admin.ModelAdmin)
