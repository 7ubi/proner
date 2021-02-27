from django import template
from project.models import *

register = template.Library()


@register.inclusion_tag('generic/sidebar_projects.html', takes_context=True)
def show_projects(context):
    request = context['request']
    print(request.user)
    print(Project.objects.filter(creator=request.user))
    return {'projects': Project.objects.filter(creator=request.user)}
