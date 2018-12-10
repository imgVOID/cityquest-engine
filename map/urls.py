"""mushrooms URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from djgeojson.views import GeoJSONLayerView

from django.views.decorators.cache import cache_page


from . import views
from .models import FirstQuestPolygon, FirstQuestMarker, SecondQuestPolygon, SecondQuestMarker


urlpatterns = [
    url(r'^admin/$', admin.site.urls),
    url(r'^accounts/$', include('django.contrib.auth.urls')),
    url(r'^first/$', views.first, name='first'),
    url(r'^second/$', views.second, name='second'),
    url(r'^levelUp/(?P<quest>\w+)$', views.levelUp, name='levelUp'),
    url(r'^testreset/(?P<quest>\w+)$', views.testreset, name='testreset'),
    url(r'^$', cache_page(600)(views.quest_list), name='quest_list'),
    url(r'^1marker.geojson$', views.marker1, name='1marker'),
    url(r'^1polygon.geojson$', views.polygon1, name='1polygon'),
    url(r'^2polygon.geojson$', views.polygon2, name='2polygon'),
    url(r'^2marker.geojson$', GeoJSONLayerView.as_view(model=SecondQuestMarker, properties=('title', 'description', 'picture_url','icon','level')), name='2marker')
] #+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)