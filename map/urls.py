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
from .models import MushroomSpot, Point


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^account/', include('django.contrib.auth.urls')),
    url(r'^$', views.home, name='home'),
    url(r'^level1complete/', views.level1complete, name='level1complete'),
    url(r'^level2complete/', views.level2complete, name='level2complete'),
    url(r'^testreset/', views.testreset, name='testreset'),
    url(r'^data.geojson$', GeoJSONLayerView.as_view(model=MushroomSpot, properties=('title', 'description', 'picture','color','num')), name='data'),
    url(r'^point.geojson$', GeoJSONLayerView.as_view(model=Point, properties=('title', 'description', 'picture_url','icon','num')), name='point')
] #+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)