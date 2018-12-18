from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from .models import Quest, Polygon, Marker, FirstQuestPolygon, SecondQuestPolygon, FirstQuestMarker, SecondQuestMarker
from django.contrib.auth.models import Group, User
from .forms import SignUpForm

import json
from django.http import JsonResponse
from djgeojson.serializers import Serializer as GeoJSONSerializer

from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.core.cache.utils import make_template_fragment_key


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('quest_list')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})
    
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
        count = Quest.objects.all().count() + 1
        progress = [0]
        for i in range(1,count):
            level_field_str = 'id' + str(i)
            progress.append(int(float(getattr(user.profile, level_field_str))/float(Polygon.objects.filter(quest=i).count())*100.0))
        cache.set(redis_key, progress, timeout=1)

    data = {
        'quest_id':quest_id,
        'title':title,
        'level':level,
        'progress':progress,
        'username':user.username,
        'full_name': '{} {}'.format(user.first_name, user.last_name)
    }
    return JsonResponse(data)

@login_required(login_url='/login/')
def first(request):
    user = request.user
    quest=1
    level = None
    if user.is_authenticated and user.groups.filter(name=quest):
        level = user.profile.id1
    else:
        level = 1

    redis_key = 'center1_'+str(user.username)
    center = cache.get(redis_key)
    if not center:
        polygon_points = FirstQuestPolygon.objects.get(level=level).geom['coordinates'][0]
        center = (sum((p[1] for p in polygon_points)) / len(polygon_points), sum((p[0] for p in polygon_points)) / len(polygon_points))
        cache.set(redis_key, center, timeout=1)
    override = {'DEFAULT_CENTER': center}
    
    redis_key = 'progress1_'+str(user.username)
    first_quest_progress = cache.get(redis_key)
    if not first_quest_progress:
        first_quest_progress = int(float(user.profile.id1)/float(FirstQuestPolygon.objects.all().count())*100.0)
        cache.set(redis_key, first_quest_progress, timeout=1)

    redis_key = 'progress2_'+str(user.username)
    second_quest_progress = cache.get(redis_key)
    if not second_quest_progress:
        second_quest_progress = int(float(user.profile.id2)/float(SecondQuestPolygon.objects.all().count())*100.0)
        cache.set(redis_key, first_quest_progress, timeout=1)

    route_type = ['walking','cycling','driving']
    return render(request, 'first_quest.html', {'level':level, 'quest':quest, 'progress1':first_quest_progress, 'progress2':second_quest_progress, 'routeTypes':route_type, 'override':override, 'center':center})

@login_required(login_url='/login/')
def second(request):
    user = request.user
    level = None
    quest = 2
    if user.is_authenticated and user.groups.filter(name=quest):
        level_field_str = 'id' + str(quest)
        level = getattr(user.profile, level_field_str)
    else:
        level = 1

    redis_key = 'center_{}_{}'.format(quest,user.username)
    center = cache.get(redis_key)
    if not center:
        polygon_points = Polygon.objects.filter(quest=2).get(level=level).geom['coordinates'][0]
        center = list((sum((p[1] for p in polygon_points)) / len(polygon_points), sum((p[0] for p in polygon_points)) / len(polygon_points)))
        cache.set(redis_key, center, timeout=1)
    override = {'DEFAULT_CENTER': center}
    
    
    
    redis_key = 'progress_{}'.format(user.username)
    progress = cache.get(redis_key)
    if not progress:
        count = Quest.objects.all().count() + 1
        progress = []
        for i in range(1,count):
            level_field_str = 'id' + str(i)
            progress.append(int(float(getattr(user.profile, level_field_str))/float(Polygon.objects.filter(quest=i).count())*100.0))
        cache.set(redis_key, progress, timeout=1)
    
    redis_key = 'progress{}_{}'.format(1,user.username)
    first_quest_progress = cache.get(redis_key)
    if not first_quest_progress:
        first_quest_progress = int(float(user.profile.id1)/float(FirstQuestPolygon.objects.all().count())*100.0)
        cache.set(redis_key, first_quest_progress, timeout=1)

    redis_key = 'progress2_'+str(user.username)
    second_quest_progress = cache.get(redis_key)
    if not second_quest_progress:
        second_quest_progress = int(float(user.profile.id2)/float(SecondQuestPolygon.objects.all().count())*100.0)
        cache.set(redis_key, first_quest_progress, timeout=1)

    route_type = ['walking','cycling','driving']
    return render(request, 'second_quest.html', {'level':level, 'quest':quest, 'progress1':first_quest_progress, 'progress2':second_quest_progress, 'routeTypes':route_type, 'override':override, 'center':center})

@login_required(login_url='/login/')
def quest_list(request):
    user = request.user
    override = {'DEFAULT_ZOOM': 12,'TILES':[('Black','https://{s}.basemaps.cartocdn.com/dark_nolabels/{z}/{x}/{y}{r}.png', {'attribution': ''}),('Watercolor','http://{s}.tile.stamen.com/watercolor/{z}/{x}/{y}.jpg', {'attribution': ''})]}
    redis_key = 'progress1_'+str(user.username)
    first_quest_progress = cache.get(redis_key)
    if not first_quest_progress:
        first_quest_progress = int(float(user.profile.id1)/float(FirstQuestPolygon.objects.all().count())*100.0)
        cache.set(redis_key, first_quest_progress, timeout=1)

    redis_key = 'progress2_'+str(user.username)
    second_quest_progress = cache.get(redis_key)
    if not second_quest_progress:
        second_quest_progress = int(float(user.profile.id2)/float(SecondQuestPolygon.objects.all().count())*100.0)
        cache.set(redis_key, first_quest_progress, timeout=1)
    return render(request, 'quest_list.html', {'progress1':first_quest_progress, 'progress2':second_quest_progress, 'override':override})

@login_required(login_url='/login/')
def levelUp(request, quest):
    user = request.user
    name = str(quest)
    if user.is_authenticated:
        if user.groups.filter(name=name):
            level_field_str = 'id' + name
            level = getattr(user.profile, level_field_str)
            if level == 1:
                setattr(user.profile, level_field_str, 2)
                user.profile.save()
                user.save()
            elif level == 2:
                setattr(user.profile, level_field_str, 1)
                user.profile.save()
                user.save()
            redis_key = make_template_fragment_key('mapdata_first',[request.user.username])
            cache.delete(redis_key)
            redis_key = 'center'+str(quest)+'_'+str(user.username)
            cache.delete(redis_key)
            redis_key = 'progress'+str(quest)+'_'+str(user.username)
            cache.delete(redis_key)
            url = '/'+quest+'/'
            return redirect(url)
        else:
            url = '/'+quest+'/'
            return redirect(url)
    else:
        return redirect('/')

@login_required(login_url='/login/')
def testreset(request, quest):
    user = request.user
    if user.is_authenticated:
        if quest == 'first_quest':
            user.profile.id1 = 1
            user.save()
            key = make_template_fragment_key('mapdata_first',[request.user.username])
            cache.delete(key)
            key = 'center1_'+str(user.username)
            cache.delete(key)
            return redirect('/first/')
        elif quest == 'second_quest':
            user.profile.id2 = 1
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

def polygon(request):
    #redis_key = 'polygon'
    #polygon = cache.get(redis_key)
    #if not polygon:
    polygon = GeoJSONSerializer().serialize(Polygon.objects.all(), use_natural_keys=True, with_modelname=False)
    #   cache.set(redis_key, polygon, timeout=None)
    return JsonResponse(json.loads(polygon))

def marker(request):
    #redis_key = 'polygon'
    #polygon = cache.get(redis_key)
    #if not polygon:
    marker = GeoJSONSerializer().serialize(Marker.objects.all(), use_natural_keys=True, with_modelname=False)
    #   cache.set(redis_key, polygon, timeout=None)
    return JsonResponse(json.loads(marker))