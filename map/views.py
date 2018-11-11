from django.shortcuts import render
from django.contrib.auth.models import Group
from django.shortcuts import redirect

#{% load geojson_tags %}

def home(request):
    username = None
    user1 = None
    if request.user.is_authenticated:
        username = request.user.username
        user1 = request.user
    groups = []
    for g in request.user.groups.all():
        groups.append(g.name)
    if len(groups) > 0:
        groups=groups[0]
    else:
        groups="0"
    return render(request, 'index.html', {'group':groups})

def level1complete(request):
    username = None
    if request.user.is_authenticated:
        username = request.user
    groupname = []
    for g in request.user.groups.all():
        groupname.append(g.name)
    if groupname[0] == '0':
        newGroup = Group.objects.get(name='1') 
        previousGroup = Group.objects.get(name='0') 
        username.groups.add(newGroup)
        username.groups.remove(previousGroup)
    return redirect('/')

def level2complete(request):
    username = None
    if request.user.is_authenticated:
        username = request.user
    groupname = []
    for g in request.user.groups.all():
        groupname.append(g.name)
    if groupname[0] == '1':
        newGroup = Group.objects.get(name='2') 
        previousGroup = Group.objects.get(name='1') 
        username.groups.add(newGroup)
        username.groups.remove(previousGroup)
    return redirect('/')

def testreset(request):
    username = None
    if request.user.is_authenticated:
        username = request.user
    for g in request.user.groups.all():
        username.groups.remove(g.name)
    newGroup = Group.objects.get(name='0') 
    username.groups.add(newGroup)
    return redirect('/')
