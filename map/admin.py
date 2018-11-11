from leaflet.admin import LeafletGeoAdmin
from django.contrib import admin
from guardian.admin import GuardedModelAdmin

from . import models as mushrooms_models


admin.site.register(mushrooms_models.MushroomSpot,GuardedModelAdmin)
admin.site.register(mushrooms_models.Point, LeafletGeoAdmin)
