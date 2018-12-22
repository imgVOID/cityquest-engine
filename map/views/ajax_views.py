from django.contrib.auth.decorators import login_required
from ..models import Quest, Polygon, Marker
from django.contrib.auth.models import User

import json
from django.http import JsonResponse
from djgeojson.serializers import Serializer as GeoJSONSerializer

from django.core.cache import cache


@login_required(login_url='/login/')
def profile(request):
    quest_id = request.GET.get('quest', None)
    user = request.user
    quest = Quest.objects.get(id=quest_id)
    title = ''
    level = None
    if quest:
        title = quest.title
        desc = quest.description
        level_field_str = 'id'+quest_id
        level = getattr(user.profile, level_field_str)

    redis_key = 'progress_{}'.format(user.username)
    progress = cache.get(redis_key)
    if not progress:
        percents = []
        quests_status = []
        for i in range(1, Quest.objects.all().count()+1):
            level_field_str = 'id' + str(i)
            if user.groups.filter(name=i):
                percents.append(int(float(getattr(user.profile, level_field_str))/float(Polygon.objects.filter(quest=i).count())*100.0))
                quests_status.append([1,''])
            else:
                percents.append(0)
                quests_status.append([0,'BUY!'])
        titles = list(Quest.objects.values_list("title", flat=True))
        progress = [0] + [{'title':titles[i], 'progress':percents[i], 'status':quests_status[i]} for i in range(0,len(titles))]
        cache.set(redis_key, progress, timeout=60000)
    data = {
        'quest_id':int(quest_id),
        'title':title,
        'level':level,
        'progress':progress,
        'username':user.username,
        'full_name': '{} {}'.format(user.first_name, user.last_name),
    }
    return JsonResponse(data)


def validate_username(request):
    username = request.GET.get('username', None)
    redis_key = 'all_users'
    usernames = cache.get(redis_key)
    if not usernames:
        usernames = User.objects.all()
        cache.set(redis_key, usernames, timeout=90)
    data = {
        'is_taken': usernames.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)

def json_polygons():
    return GeoJSONSerializer().serialize(Polygon.objects.all(), use_natural_keys=True, with_modelname=False)

def json_markers():
    return GeoJSONSerializer().serialize(Marker.objects.all(), use_natural_keys=True, with_modelname=False)

def polygon(request):
    redis_key = 'polygons'
    polygon = cache.get(redis_key)
    if not polygon:
        polygon = json_polygons()
        cache.set(redis_key, polygon, timeout=None)
    return JsonResponse(json.loads(polygon))

def marker(request):
    redis_key = 'markers'
    marker = cache.get(redis_key)
    if not marker:
        marker = json_markers()
        cache.set(redis_key, marker, timeout=None)
    return JsonResponse(json.loads(marker))
