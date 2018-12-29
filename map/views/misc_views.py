from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from ..models import Quest, Polygon, Marker
from django.shortcuts import render, redirect


@login_required(login_url='/login/')
def quest_list(request):
    user = request.user
    override = {'DEFAULT_ZOOM': 12,'TILES':[('Black','https://{s}.basemaps.cartocdn.com/dark_nolabels/{z}/{x}/{y}{r}.png', {'attribution': ''}),('Watercolor','http://{s}.tile.stamen.com/watercolor/{z}/{x}/{y}.jpg', {'attribution': ''})]}
    redis_key = 'all_quests'
    all_quests = cache.get(redis_key)
    if not all_quests:
        all_quests = [str(i) for i in range(1,Quest.objects.all().count()+1)]
        cache.set(redis_key, all_quests, timeout=None)

    redis_key = 'quests_descs'
    quests_descs = cache.get(redis_key)
    if not quests_descs:
        quests_descs = [0] + list(Quest.objects.all().values_list("description", flat=True))
        cache.set(redis_key, quests_descs, timeout=None)
    colors = ['white','green','red','blue','yellow','orange','purple','aqua','saddlebrown'][0:len(quests_descs)]
    redis_key = 'progress_{}'.format(user.username)
    progress = cache.get(redis_key)
    if not progress:
        progress = 0

    quests_count = len(quests_descs)-1

    return render(request, 'quest_list.html', {'override':override,'descs':quests_descs, 'quests_count':quests_count,'colors':colors,'progress':progress,'all_quests':all_quests})

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
            redis_key = make_template_fragment_key('mapdata',[quest,request.user.username])
            cache.delete(redis_key)
            redis_key = 'progress_{}'.format(user.username)
            cache.delete(redis_key)
            url = '/{}/'.format(quest)
            return redirect(url)
        else:
            url = '/{}/'.format(quest)
            return redirect(url)
    else:
        return redirect('/')

@login_required(login_url='/login/')
def testreset(request, quest):
    user = request.user
    if user.is_authenticated:
        level_field_str = 'id' + str(quest)
        setattr(user.profile, level_field_str, 1)
        user.profile.save()
        user.save()
        redis_key = make_template_fragment_key('mapdata',[quest,request.user.username])
        cache.delete(redis_key)
        redis_key = 'progress_{}'.format(user.username)
        cache.delete(redis_key)
        url = '/{}/'.format(quest)
        return redirect(url)
    else:
        return redirect('/')

@login_required(login_url='/login/')
def clear_cache(request, quest):
    cache.clear()
    return redirect('/{}/'.format(quest))