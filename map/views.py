from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from .models import FirstQuestPolygon, SecondQuestPolygon, FirstQuestMarker, SecondQuestMarker
from django.contrib.auth.models import Group

import json
from django.http import JsonResponse
from django.core.serializers import serialize
from djgeojson.serializers import Serializer as GeoJSONSerializer

from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.core.cache.utils import make_template_fragment_key


@login_required(login_url='/accounts/login/')
def first(request):
    user = request.user
    test = 1
    quest = None
    level = None
    if user.is_authenticated and user.groups.filter(name="First Quest"):
            quest='first_quest'
            level = user.profile.first_quest
    else:
        level = 1
    cache.set('first_level',level)
    first_quest_progress = int(float(user.profile.first_quest)/float(FirstQuestPolygon.objects.all().count())*100.0)
    second_quest_progress = int(float(user.profile.second_quest)/float(SecondQuestPolygon.objects.all().count())*100.0)
    route_type = ['walking','cycling','driving']
    return render(request, 'first_quest.html', {'level':level, 'quest':quest, 'test':test, 'progress1':first_quest_progress, 'progress2':second_quest_progress, 'routeTypes':route_type})

@login_required(login_url='/accounts/login/')
def second(request):
    user = request.user
    test = 2
    level = None
    quest = None
    if not level:
        if user.is_authenticated and user.groups.filter(name="Second Quest"):
            level = user.profile.second_quest
            quest = 'second_quest'
        else:
            level = 1
    
    first_quest_progress = int(float(user.profile.first_quest)/float(FirstQuestPolygon.objects.all().count())*100.0)
    second_quest_progress = int(float(user.profile.second_quest)/float(SecondQuestPolygon.objects.all().count())*100.0)
    route_type = ['walking','cycling','driving']
    return render(request, 'second_quest.html', {'level':level, 'quest':quest, 'test':test, 'progress1':first_quest_progress, 'progress2':second_quest_progress, 'routeTypes':route_type})

def first1(request):
    user = request.user
    if user.is_authenticated:
        if user.groups.filter(name="First Quest") \
        and user.profile.first_quest == 1:
            user.profile.first_quest = 2
            user.save()
            key = make_template_fragment_key('mapdata_first',[request.user.username])
            cache.delete(key)
    return redirect('/first/')

def first2(request):
    user = request.user
    if user.is_authenticated:
        if user.groups.filter(name="First Quest") \
        and user.profile.first_quest == 1:
            user.profile.first_quest = 3
            user.save()
            key = make_template_fragment_key('mapdata_first',[request.user.username])
            cache.delete(key)
    return redirect('/first/')

def firsttestreset(request):
    user = request.user
    if user.is_authenticated:
        user.profile.first_quest = 1
        user.save()
        key = make_template_fragment_key('mapdata_first',[request.user.username])
        cache.delete(key)
    return redirect('/first/')
    
def second1(request):
    user = request.user
    if user.is_authenticated:
        if user.groups.filter(name="Second Quest") \
        and user.profile.second_quest == 1:
            user.profile.second_quest = 2
            user.save()
            key = make_template_fragment_key('mapdata_second',[request.user.username])
            cache.delete(key)
    return redirect('/second/')

def second2(request):
    user = request.user
    if user.is_authenticated:
        if user.groups.filter(name="Second Quest") \
        and user.profile.second_quest == 2:
            user.profile.second_quest = 3
            user.save()
            key = make_template_fragment_key('mapdata_second',[request.user.username])
            cache.delete(key)
    return redirect('/second/')

def secondtestreset(request):
    user = request.user
    if user.is_authenticated:
        user.profile.second_quest = 1
        user.save()
        key = make_template_fragment_key('mapdata_second',[request.user.username])
        cache.delete(key)
    return redirect('/second/')

@login_required(login_url='/accounts/login/')
def quest_list(request):
    user = request.user
    first_quest_geo = FirstQuestMarker.objects.all()
    override = {'DEFAULT_ZOOM': 12,'TILES':[('Black','https://{s}.basemaps.cartocdn.com/dark_nolabels/{z}/{x}/{y}{r}.png', {'attribution': ''}),('Watercolor','http://{s}.tile.stamen.com/watercolor/{z}/{x}/{y}.jpg', {'attribution': ''})]}
    first_quest_progress = int(float(user.profile.first_quest)/float(FirstQuestPolygon.objects.all().count())*100.0)
    second_quest_progress = int(float(user.profile.second_quest)/float(SecondQuestPolygon.objects.all().count())*100.0)
    return render(request, 'quest_list.html', {'progress1':first_quest_progress, 'progress2':second_quest_progress, 'override':override})


def marker1(request):
    redis_key = 'marker1'
    marker1 = cache.get(redis_key)  # getting value for given key from redis
    if not marker1:
       marker1 = GeoJSONSerializer().serialize(FirstQuestMarker.objects.all(), use_natural_keys=True, with_modelname=True)
       cache.set(redis_key, marker1)
    return JsonResponse(json.loads(marker1))

def polygon1(request):
    redis_key = 'polygon1'
    polygon1 = cache.get(redis_key)
    if not polygon1:
        polygon1 = GeoJSONSerializer().serialize(FirstQuestPolygon.objects.all(), use_natural_keys=True, with_modelname=False)
        cache.set(redis_key, polygon1)
    return JsonResponse(json.loads(polygon1))
    
def marker2(request):
    redis_key = 'marker2'
    marker2 = cache.get(redis_key)  
    if not marker2:
       marker2 = GeoJSONSerializer().serialize(FirstQuestMarker.objects.all(), use_natural_keys=True, with_modelname=True)
       cache.set(redis_key, marker1)
    return JsonResponse(json.loads(marker1))

def polygon2(request):
    redis_key = 'polygon2'
    polygon2 = cache.get(redis_key)
    if not polygon2:
       polygon2 = GeoJSONSerializer().serialize(SecondQuestPolygon.objects.all(), use_natural_keys=True, with_modelname=False)
       cache.set(redis_key, polygon2)
    return JsonResponse(json.loads(polygon2))
    
