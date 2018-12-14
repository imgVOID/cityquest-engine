from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from djgeojson.views import GeoJSONLayerView

from django.contrib.auth import views as auth_views

from django.views.decorators.cache import cache_page


from . import views
from .models import FirstQuestPolygon, FirstQuestMarker, SecondQuestPolygon, SecondQuestMarker


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/login/'}, name='logout'),
#    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^first/$', views.first, name='first'),
    url(r'^second/$', views.second, name='second'),
    url(r'^levelUp/(?P<quest>\w+)$', views.levelUp, name='levelUp'),
    url(r'^testreset/(?P<quest>\w+)$', views.testreset, name='testreset'),
    url(r'^$', views.quest_list, name='quest_list'),
    url(r'^1marker.geojson$', views.marker1, name='1marker'),
    url(r'^1polygon.geojson$', views.polygon1, name='1polygon'),
    url(r'^2polygon.geojson$', views.polygon2, name='2polygon'),
    url(r'^2marker.geojson$', GeoJSONLayerView.as_view(model=SecondQuestMarker, properties=('title', 'description', 'picture_url','icon','level')), name='2marker')
] #+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)