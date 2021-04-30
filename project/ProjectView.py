from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import *
import json
from django.core import serializers


@login_required
def create_project_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')

        if Project.objects.filter(name=name, creator=request.user).exists():
            return HttpResponse(json.dumps({'success': False, 'error': 'Project already exists'}),
                                content_type="application/json")

        p = Project(name=name, creator=request.user)
        p.save()
        return HttpResponse(json.dumps({'success': True, 'slug': Project.objects.get(name=name, creator=request.user).slug}), content_type="application/json")
    return render(request, 'project/create_project.html')


@login_required
def project_view(request, slug):
    project = Project.objects.get(slug=slug, creator=request.user)
    notes = Note.objects.filter(creator=request.user, project=project)
    return render(request, 'Project/show_project.html', {'project': project, 'notes': notes})


@login_required
def create_task_view(request, slug):
    name = request.POST.get('name')
    text = request.POST.get('text')
    project = Project.objects.get(slug=slug)
    if Note.objects.filter(name=name).exists():
        return HttpResponse(json.dumps({'success': False}), content_type='application/json')
    else:
        note = Note(name=name, project=project, text=text, creator=request.user)
        note.save()
    return HttpResponse(json.dumps({'success': True}), content_type='application/json')


@login_required
def get_note(request):
    return HttpResponse(serializers.serialize("json", Note.objects.filter(name=request.GET.get('name'))),
                        content_type='application/json')
