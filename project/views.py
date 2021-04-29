from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
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



