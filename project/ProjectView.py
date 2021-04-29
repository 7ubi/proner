from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import *
import json

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

@login_required
def project_view(request, slug):
    project = Project.objects.get(slug=slug, creator=request.user)
    labels = Label.objects.filter(creator=request.user)
    tasks = Task.objects.filter(project=project)

    tasks_with_label = [[] for x in range(len(labels))]
    print(tasks_with_label)
    for i in range(len(labels)):
        label = labels[i]
        for task in tasks:
            if task.labels == label:
                tasks_with_label[i].append(task)
    print(tasks_with_label)
    return render(request, 'Project/show_project.html', {'project': project,
                                                         'labels': labels,
                                                         'tasks_by_label': tasks_with_label})



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