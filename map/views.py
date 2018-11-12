from django.shortcuts import render
from django.contrib.auth.models import Group
from django.shortcuts import redirect
#from .models import User

#{% load geojson_tags %}

#def home(request){
    
#}

def first(request):
    user = request.user
    test = 1
    quest = None
    level = None
    test = 1
    if user.is_authenticated:
#       !BECAUSE DJANGO GUARDIAN ANONYMOUS USER!
        if len(user.username) > 0 \
        and user.groups.filter(name="First Quest"):
            quest='first_quest'
            level = user.profile.first_quest
        else:
            level=1
    else:
        level = 1
    return render(request, 'index.html', {'level':level, 'quest':quest, 'test':test})

def second(request):
    user = request.user
    test = 2
    quest = None
    level = None
    if user.is_authenticated:
#       !BECAUSE DJANGO GUARDIAN ANONYMOUS USER!
        if len(user.username) > 0 \
        and user.groups.filter(name="Second Quest"):
            level = user.profile.second_quest
            quest = 'second_quest'
        else:
            level=1
    else:
        level = 1
    return render(request, 'index.html', {'level':level, 'quest':quest, 'test':test})

def first1(request):
    user = request.user
    if user.is_authenticated:
        if user.groups.filter(name="First Quest") \
        and user.profile.first_quest == 1:
                user.profile.first_quest = 2
                user.save()
    return redirect('/first/')

def first2(request):
    user = request.user
    if user.is_authenticated:
        if user.groups.filter(name="First Quest") \
        and user.profile.first_quest == 1:
            user.profile.first_quest = 3
            user.save()
    return redirect('/first/')

def firsttestreset(request):
    user = request.user
    if user.is_authenticated:
        user.profile.first_quest = 1
        user.save()
    return redirect('/first/')
    
def second1(request):
    user = request.user
    if user.is_authenticated:
        if user.groups.filter(name="Second Quest") \
        and user.profile.second_quest == 1:
            user.profile.second_quest = 2
            user.save()
    return redirect('/second/')

def second2(request):
    user = request.user
    if user.is_authenticated:
        if user.groups.filter(name="Second Quest") \
        and user.profile.second_quest == 1:
            user.profile.second_quest = 2
            user.save()
    return redirect('/second/')

def secondtestreset(request):
    user = request.user
    if user.is_authenticated:
        user.profile.second_quest = 1
        user.save()
    return redirect('/second/')
