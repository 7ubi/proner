from django.shortcuts import render, redirect, HttpResponse
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
        return HttpResponse(
            json.dumps({'success': True, 'slug': Project.objects.get(name=name, creator=request.user).slug}),
            content_type="application/json")
    return render(request, 'project/create_project.html')


@login_required
def project_view(request, slug):
    project = Project.objects.get(slug=slug, creator=request.user)
    notes = Note.objects.filter(creator=request.user, project=project)
    return render(request, 'Project/show_project.html', {'project': project, 'notes': notes})


@login_required
def create_note_view(request, slug):
    name = request.POST.get('name')
    text = request.POST.get('text')
    project = Project.objects.get(slug=slug)
    if Note.objects.filter(name=name).exists():
        return HttpResponse(json.dumps({'id': 0}), content_type='application/json')

    note = Note(name=name, project=project, text=text, creator=request.user)
    note.save()
    return HttpResponse(json.dumps({'id': note.id}), content_type='application/json')


@login_required
def get_note(request):
    return HttpResponse(serializers.serialize("json", Note.objects.filter(id=request.GET.get('id'))),
                        content_type='application/json')


@login_required
def delete_project(request):
    slug = request.POST.get("project")
    project = Project.objects.filter(creator=request.user, slug=slug)
    project.delete()

    return redirect("/")


def edit_project(request):
    slug = request.POST.get("project")
    project = Project.objects.filter(creator=request.user, slug=slug).first()
    name = request.POST.get("name")
    if Project.objects.filter(creator=request.user, name=name).exists():
        return HttpResponse(json.dumps({'slug': ''}), content_type='application/json')
    else:
        project.name = name

        s = slugify(project.name)

        slugExists = Project.objects.filter(slug=s).exists()

        n = 1
        while slugExists:
            s = slugify(project.name + str(n))
            slugExists = Project.objects.filter(slug=s).exists()
            n += 1

        project.slug = s
        project.save()

        return HttpResponse(json.dumps({'slug': s}), content_type='application/json')


@login_required
def delete_note(request):
    print(request.POST.get("note"))
    noteId = int(float(request.POST.get("note")))

    note = Note.objects.filter(id=noteId)
    note.delete()

    return HttpResponse(json.dumps({'id': noteId}), content_type='application/json')


@login_required
def edit_note(request):
    noteId = request.POST.get('note')
    name = request.POST.get('name')
    text = request.POST.get('text')

    note = Note.objects.filter(id=noteId).first()
    note.name = name
    note.text = text

    note.save()

    return HttpResponse(serializers.serialize("json", Note.objects.filter(id=noteId)), content_type='application/json')