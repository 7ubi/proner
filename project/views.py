from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import *
import json


# Create your views here.
@login_required
def home_view(request):
    return render(request, 'generic/home.html')


def logout_view(request):
    logout(request)
    return redirect("/login")


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            username = request.POST.get("username")
            password = request.POST.get("password")

            user = authenticate(request, username=username, password=password)

            if user:
                login(request, user)
                return redirect('/')
            else:
                try:
                    User.objects.get(username=username)
                    return render(request, 'login/login.html', {'error': 'Password invalid!'})
                except:
                    return render(request, 'login/login.html', {'error': 'User does not exist!'})
    return render(request, 'login/login.html')


@login_required
def create_project_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if Project.objects.filter(name=name, creator=request.user).exists():
            return HttpResponse(json.dumps({'success': False, 'error': 'Project already exists'}),
                                content_type="application/json")

        p = Project(name=name, creator=request.user)
        p.save()
        return HttpResponse(json.dumps({'success': True}), content_type="application/json")
    return render(request, 'project/create_project.html')

def project_view(request, slug):
    try:
        project = Project.objects.get(slug=slug)
        return render(request, 'Project/show_project.html', {'project': project})
    except:
        redirect('/')

def create_task_view(request, slug):
    name = request.POST.get('name')

    project = Project.objects.get(slug=slug)
    task = Task(name=name, creator=request.user, project=project)
    task.save()

    return HttpResponse(json.dumps({'success': True}), content_type="application/json")
