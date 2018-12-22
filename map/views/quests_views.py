from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from ..models import Quest, Polygon
from .ajax_views import json_polygons, json_markers

from django.core.cache import cache

@login_required(login_url='/login/')
def first(request):
    quest = 1
    user = request.user
    route_type = ['walking','cycling','driving']
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

    redis_key = 'polygons'
    polygon = cache.get(redis_key)
    if not polygon:
        polygon = json_polygons()
        cache.set(redis_key, polygon, timeout=None)

    redis_key = 'markers'
    marker = cache.get(redis_key)
    if not marker:
        marker = json_markers()
        cache.set(redis_key, marker, timeout=None)

    return render(request, 'first_quest.html', {
        'level':level, 'quest':quest, 'routeTypes':route_type, 'override':override,
        'center':center, 'all_quests':all_quests, 'polygon':polygon,'marker':marker})


@login_required(login_url='/login/')
def second(request):
    quest = 2
    user = request.user
    route_type = ['walking','cycling','driving']
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

    redis_key = 'polygons'
    polygon = cache.get(redis_key)
    if not polygon:
        polygon = json_polygons()
        cache.set(redis_key, polygon, timeout=None)

    redis_key = 'markers'
    marker = cache.get(redis_key)
    if not marker:
        marker = json_markers()
        cache.set(redis_key, marker, timeout=None)

    return render(request, 'second_quest.html', {
        'level':level, 'quest':quest, 'routeTypes':route_type, 'override':override,
        'center':center, 'all_quests':all_quests, 'polygon':polygon,'marker':marker})

