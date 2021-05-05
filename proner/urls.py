"""proner URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from project.views import *
from project.ProjectView import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view),
    path('logout', logout_view),
    path('signup', register_view),
    path('signup/check_username', check_username),
    path('projects/<slug:slug>', project_view),
    path('projects/<slug:slug>/create_task', create_note_view),
    path('deleteProject', delete_project),
    path('login/', login_view),
    path('create-project/', create_project_view),
    path('delete-note', delete_note),
    path('edit-note', edit_note),
    path('edit-project', edit_project),
    path('getNote/', get_note),
]
