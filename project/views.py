from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate

# Create your views here.
def home_view(request):
    return render(request, 'generic/base.html')


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
                return render(request, 'login/login.html', {'error': 'Username or Password invalid!'})
    return render(request, 'login/login.html')