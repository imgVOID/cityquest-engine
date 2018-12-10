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
    quest='first_quest'
    level = None
    if user.is_authenticated and user.groups.filter(name="First Quest"):
        level = user.profile.first_quest
    else:
        level = 1

    redis_key = 'center1_'+str(user.username)
    center = cache.get(redis_key)
    if not center:
        polygon_points = FirstQuestPolygon.objects.get(level=level).geom['coordinates'][0]
        center = (sum((p[1] for p in polygon_points)) / len(polygon_points), sum((p[0] for p in polygon_points)) / len(polygon_points))
        cache.set(redis_key, center, timeout=60000)
    override = {'DEFAULT_CENTER': center}
    
    redis_key = 'progress1_'+str(user.username)
    first_quest_progress = cache.get(redis_key)
    if not first_quest_progress:
        first_quest_progress = int(float(user.profile.first_quest)/float(FirstQuestPolygon.objects.all().count())*100.0)
        cache.set(redis_key, first_quest_progress, timeout=60000)

    redis_key = 'progress2_'+str(user.username)
    second_quest_progress = cache.get(redis_key)
    if not second_quest_progress:
        second_quest_progress = int(float(user.profile.second_quest)/float(SecondQuestPolygon.objects.all().count())*100.0)
        cache.set(redis_key, first_quest_progress, timeout=60000)

    route_type = ['walking','cycling','driving']
    return render(request, 'first_quest.html', {'level':level, 'quest':quest, 'progress1':first_quest_progress, 'progress2':second_quest_progress, 'routeTypes':route_type, 'override':override, 'center':center})

@login_required(login_url='/accounts/login/')
def second(request):
    user = request.user
    level = None
    quest = 'second_quest'
    if user.is_authenticated and user.groups.filter(name="Second Quest"):
        level = user.profile.second_quest
    else:
        level = 1

    redis_key = 'center2_'+str(user.username)
    center = cache.get(redis_key)
    if not center:
        polygon_points = SecondQuestPolygon.objects.get(level=level).geom['coordinates'][0]
        center = list((sum((p[1] for p in polygon_points)) / len(polygon_points), sum((p[0] for p in polygon_points)) / len(polygon_points)))
        cache.set(redis_key, center, timeout=60000)
    override = {'DEFAULT_CENTER': center}
    
    redis_key = 'progress1_'+str(user.username)
    first_quest_progress = cache.get(redis_key)
    if not first_quest_progress:
        first_quest_progress = int(float(user.profile.first_quest)/float(FirstQuestPolygon.objects.all().count())*100.0)
        cache.set(redis_key, first_quest_progress, timeout=60000)

    redis_key = 'progress2_'+str(user.username)
    second_quest_progress = cache.get(redis_key)
    if not second_quest_progress:
        second_quest_progress = int(float(user.profile.second_quest)/float(SecondQuestPolygon.objects.all().count())*100.0)
        cache.set(redis_key, first_quest_progress, timeout=60000)

    route_type = ['walking','cycling','driving']
    return render(request, 'second_quest.html', {'level':level, 'quest':quest, 'progress1':first_quest_progress, 'progress2':second_quest_progress, 'routeTypes':route_type, 'override':override, 'center':center})

@login_required(login_url='/accounts/login/')
def quest_list(request):
    user = request.user
    override = {'DEFAULT_ZOOM': 12,'TILES':[('Black','https://{s}.basemaps.cartocdn.com/dark_nolabels/{z}/{x}/{y}{r}.png', {'attribution': ''}),('Watercolor','http://{s}.tile.stamen.com/watercolor/{z}/{x}/{y}.jpg', {'attribution': ''})]}

    redis_key = 'progress1_'+str(user.username)
    first_quest_progress = cache.get(redis_key)
    if not first_quest_progress:
        first_quest_progress = int(float(user.profile.first_quest)/float(FirstQuestPolygon.objects.all().count())*100.0)
        cache.set(redis_key, first_quest_progress, timeout=60000)

    redis_key = 'progress2_'+str(user.username)
    second_quest_progress = cache.get(redis_key)
    if not second_quest_progress:
        second_quest_progress = int(float(user.profile.second_quest)/float(SecondQuestPolygon.objects.all().count())*100.0)
        cache.set(redis_key, first_quest_progress, timeout=60000)
    return render(request, 'quest_list.html', {'progress1':first_quest_progress, 'progress2':second_quest_progress, 'override':override})

@login_required(login_url='/accounts/login/')
def levelUp(request, quest):
    user = request.user
    if user.is_authenticated:
        if quest == 'first_quest':
            if user.groups.filter(name="First Quest"):
                if user.profile.first_quest == 1:
                    user.profile.first_quest = 2
                    user.save()
                elif user.profile.first_quest == 2:
                    user.profile.first_quest = 3
                    user.save()
                redis_key = make_template_fragment_key('mapdata_first',[request.user.username])
                cache.delete(redis_key)
                redis_key = 'center1_'+str(user.username)
                cache.delete(redis_key)
                redis_key = 'progress1_'+str(user.username)
                cache.delete(redis_key)
                return redirect('/first/')
            else:
                return redirect('/first/')
        elif quest == 'second_quest':
            if user.groups.filter(name="Second Quest"):
                if user.profile.second_quest == 1:
                    user.profile.second_quest = 2
                    user.save()
                elif user.profile.second_quest == 2:
                    user.profile.second_quest = 3
                    user.save()
                key = make_template_fragment_key('mapdata_second',[request.user.username])
                cache.delete(key)
                key = 'center2_'+str(user.username)
                cache.delete(key)
                redis_key = 'progress2_'+str(user.username)
                cache.delete(redis_key)
                return redirect('/second/')
            else:
                return redirect('/second/')
        else:
            return redirect('/')
    else:
        return redirect('/')

@login_required(login_url='/accounts/login/')
def testreset(request, quest):
    user = request.user
    if user.is_authenticated:
        if quest == 'first_quest':
            user.profile.first_quest = 1
            user.save()
            key = make_template_fragment_key('mapdata_first',[request.user.username])
            cache.delete(key)
            key = 'center1_'+str(user.username)
            cache.delete(key)
            return redirect('/first/')
        elif quest == 'second_quest':
            user.profile.second_quest = 1
            user.save()
            key = make_template_fragment_key('mapdata_second',[request.user.username])
            cache.delete(key)
            key = 'center2_'+str(user.username)
            cache.delete(key)
            return redirect('/second/')
    else:
        return redirect('/')

def marker1(request):
    redis_key = 'marker1'
    marker1 = cache.get(redis_key)
    if not marker1:
       marker1 = GeoJSONSerializer().serialize(FirstQuestMarker.objects.all(), use_natural_keys=True, with_modelname=True)
       cache.set(redis_key, marker1, timeout=None)
    return JsonResponse(json.loads(marker1))

def polygon1(request):
    redis_key = 'polygon1'
    polygon1 = cache.get(redis_key)
    if not polygon1:
        polygon1 = GeoJSONSerializer().serialize(FirstQuestPolygon.objects.all(), use_natural_keys=True, with_modelname=False)
        cache.set(redis_key, polygon1, timeout=None)
    return JsonResponse(json.loads(polygon1))
    
def marker2(request):
    redis_key = 'marker2'
    marker2 = cache.get(redis_key)  
    if not marker2:
       marker2 = GeoJSONSerializer().serialize(FirstQuestMarker.objects.all(), use_natural_keys=True, with_modelname=True)
       cache.set(redis_key, marker1, timeout=None)
    return JsonResponse(json.loads(marker1))

def polygon2(request):
    redis_key = 'polygon2'
    polygon2 = cache.get(redis_key)
    if not polygon2:
       polygon2 = GeoJSONSerializer().serialize(SecondQuestPolygon.objects.all(), use_natural_keys=True, with_modelname=False)
       cache.set(redis_key, polygon2, timeout=None)
    return JsonResponse(json.loads(polygon2))
    
