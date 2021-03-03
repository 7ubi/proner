from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import *
import json
from django.http import HttpResponseRedirect


# Create your views here.
@login_required
def home_view(request):
    return render(request, 'generic/home.html')


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/login")


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


def register_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        pw1 = request.POST.get('password1')
        pw2 = request.POST.get('password2')

        if pw1 == pw2:
            user = User(username=username, email=email)
            user.set_password(pw1)
            user.save()

            return HttpResponse(json.dumps({'success': True}), content_type="application/json")
        return HttpResponse(json.dumps({'success': False, 'error': 'Passwords do not match'}),
                            content_type="application/json")

    return render(request, 'login/register.html')


def check_username(request):
    if request.method == "POST":
        username = request.POST.get('username')

        if User.objects.filter(username=username).exists():
            return HttpResponse(json.dumps({'exists': True}), content_type="application/json")
        return HttpResponse(json.dumps({'exists': False}), content_type="application/json")


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
        project = Project.objects.get(slug=slug, creator=request.user)
        labels = Label.objects.filter(creator=request.user)
        return render(request, 'Project/show_project.html', {'project': project, 'labels': labels})
    except:
        return redirect('/')


def create_task_view(request, slug):
    name = request.POST.get('name')
    label_name = request.POST.get('label')

    project = Project.objects.get(slug=slug)
    task = None
    if label_name != 'No Label':
        label = Label.objects.get(name=label_name, creator=request.user)
        task = Task(name=name, creator=request.user, project=project, labels=label)
    else:
        task = Task(name=name, creator=request.user, project=project)

    task.save()

    return HttpResponse(json.dumps({'success': True}), content_type="application/json")
