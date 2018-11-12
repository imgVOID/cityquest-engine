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

from . import views
from .models import FirstQuestPolygon, FirstQuestMarker, SecondQuestPolygon, SecondQuestMarker


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^account/', include('django.contrib.auth.urls')),
#    url(r'^$', views.home, name='home'),
    url(r'^first/', views.first, name='first'),
    url(r'^second/', views.second, name='second'),
    url(r'^first1/', views.first1, name='first1'),
    url(r'^first2/', views.first2, name='first2'),
    url(r'^second1/', views.second1, name='second1'),
    url(r'^second2/', views.second2, name='second2'),
    url(r'^firsttestreset/', views.firsttestreset, name='firsttestreset'),
    url(r'^secondtestreset/', views.secondtestreset, name='secondtestreset'),
    url(r'^1polygon.geojson$', GeoJSONLayerView.as_view(model=FirstQuestPolygon, properties=('title', 'description', 'picture','color','level')), name='1polygon'),
    url(r'^1marker.geojson$', GeoJSONLayerView.as_view(model=FirstQuestMarker, properties=('title', 'description', 'picture_url','icon','level')), name='1marker'),
    url(r'^2polygon.geojson$', GeoJSONLayerView.as_view(model=SecondQuestPolygon, properties=('title', 'description', 'picture','color','level')), name='2polygon'),
    url(r'^2marker.geojson$', GeoJSONLayerView.as_view(model=SecondQuestMarker, properties=('title', 'description', 'picture_url','icon','level')), name='2marker')
] #+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)