from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User


# Create your views here.
def home_view(request):
    return render(request, 'generic/home.html')


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
