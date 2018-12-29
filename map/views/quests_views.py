from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from ..models import Quest, Polygon
from .ajax_views import json_polygons, json_markers

from django.core.cache import cache

import json

#       ________________________________________________________________
#       ****************************************************************
#       ***************************FIRST QUEST**************************
#       ****************************************************************

@login_required(login_url='/login/')
def first(request):
    quest = 1
    user = request.user
    level = None

    if user.is_authenticated and user.groups.filter(name=quest):
        level_field_str = 'id' + str(quest)
        level = getattr(user.profile, level_field_str)
    else:
        level = 1

    redis_key = 'all_quests'
    all_quests = cache.get(redis_key)
    if not all_quests:
        all_quests = [str(i) for i in range(1,Quest.objects.all().count()+1)]
        cache.set(redis_key, all_quests, timeout=None)

    redis_key = 'center_{}'.format(quest)
    center = cache.get(redis_key)
    if not center:
        levels = Polygon.objects.filter(quest=quest).count() + 1
        center = [0]
        for i in range(1, levels):
            polygon_points = Polygon.objects.filter(quest=quest).get(level=i).geom['coordinates'][0]
            one_center = list((sum((p[1] for p in polygon_points)) / len(polygon_points), sum((p[0] for p in polygon_points)) / len(polygon_points)))
            center.append(one_center)
        cache.set(redis_key, center, timeout=None)

    center = center[level]

    override = {'DEFAULT_CENTER': center}

    redis_key = 'polygon_{}_{}'.format(quest,level)
    level_polygon = cache.get(redis_key)
    if not level_polygon:
        polygon = cache.get('polygons')
        if not polygon:
            polygon = json.loads(json_polygons())
            cache.set('polygons', polygon, timeout=None)
        level_polygon = polygon
        level_polygon['features'] = list(filter(lambda x: x['properties']['quest'] == quest and x['properties']['level'] == level, polygon['features']))
        cache.set(redis_key, level_polygon, timeout=None)

    redis_key = 'marker_{}_{}'.format(quest,level)
    level_marker = cache.get(redis_key)
    if not level_marker:
        marker = cache.get('markers')
        if not marker:
            marker = json.loads(json_markers())
            cache.set(redis_key, marker, timeout=None)
        level_marker = marker
        level_marker['features'] = list(filter(lambda x: x['properties']['quest'] == quest and x['properties']['level'] < level, marker['features']))
        cache.set(redis_key, level_marker, timeout=None)

    return render(request, 'first_quest.html', {
        'level':level, 'quest':quest, 'override':override, 'center':center, 'quests_count':len(all_quests),
        'polygon':level_polygon,'marker':level_marker,'all_quests':all_quests})

#       ________________________________________________________________
#       ****************************************************************
#       ***************************SECOND QUEST**************************
#       ****************************************************************

@login_required(login_url='/login/')
def second(request):
    quest = 2
    user = request.user
    level = None

    if user.is_authenticated and user.groups.filter(name=quest):
        level_field_str = 'id' + str(quest)
        level = getattr(user.profile, level_field_str)
    else:
        level = 1

    redis_key = 'all_quests'
    all_quests = cache.get(redis_key)
    if not all_quests:
        all_quests = [str(i) for i in range(1,Quest.objects.all().count()+1)]
        cache.set(redis_key, all_quests, timeout=None)

    redis_key = 'center_{}'.format(quest)
    center = cache.get(redis_key)
    if not center:
        levels = Polygon.objects.filter(quest=quest).count() + 1
        center = [0]
        for i in range(1, levels):
            polygon_points = Polygon.objects.filter(quest=quest).get(level=i).geom['coordinates'][0]
            one_center = list((sum((p[1] for p in polygon_points)) / len(polygon_points), sum((p[0] for p in polygon_points)) / len(polygon_points)))
            center.append(one_center)
        cache.set(redis_key, center, timeout=None)

    center = center[level]

    override = {'DEFAULT_CENTER': center}

    redis_key = 'polygon_{}_{}'.format(quest,level)
    level_polygon = cache.get(redis_key)
    if not level_polygon:
        polygon = cache.get('polygons')
        if not polygon:
            polygon = json.loads(json_polygons())
            cache.set('polygons', polygon, timeout=None)
        level_polygon = polygon
        level_polygon['features'] = list(filter(lambda x: x['properties']['quest'] == quest and x['properties']['level'] == level, polygon['features']))
        cache.set(redis_key, level_polygon, timeout=None)

    redis_key = 'marker_{}_{}'.format(quest,level)
    level_marker = cache.get(redis_key)
    if not level_marker:
        marker = cache.get('markers')
        if not marker:
            marker = json.loads(json_markers())
            cache.set(redis_key, marker, timeout=None)
        level_marker = marker
        level_marker['features'] = list(filter(lambda x: x['properties']['quest'] == quest and x['properties']['level'] < level, marker['features']))
        cache.set(redis_key, level_marker, timeout=None)

    return render(request, 'second_quest.html', {
        'level':level, 'quest':quest, 'override':override, 'center':center, 'quests_count':len(all_quests),
        'polygon':level_polygon,'marker':level_marker,'all_quests':all_quests})
