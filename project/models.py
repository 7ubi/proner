from django.db import models
from django.conf import settings
from colorfield.fields import ColorField

# Create your models here.
class Label(models.Model):
    name = models.CharField(max_length=100)
    color = ColorField(default='#FFFFFF')

class Task(models.Model):
    name = models.CharField(max_length=100)
    labels = models.ForeignKey(Label, on_delete=models.SET_NULL, null=True, blank=True)

class Project(models.Model):
    name = models.CharField(max_length=100)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tasks = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True, blank=True)

