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
    url(r'grappelli/', include('grappelli.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^ajax/validate_username/$', views.validate_username, name='validate_username'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/login/'}, name='logout'),
    url(r'^ajax/profile_data/$', views.profile, name='profile'),
#    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^1/$', views.first, name='1'),
    url(r'^2/$', views.second, name='2'),
    url(r'^levelUp/(?P<quest>\d+)/$', views.levelUp, name='levelUp'),
    url(r'^testreset/(?P<quest>\d+)/$', views.testreset, name='testreset'),
    url(r'^$', views.quest_list, name='quest_list'),
    url(r'^polygon.geojson$', views.polygon, name='polygon'),
    url(r'^marker.geojson$', views.marker, name='marker')] #+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)