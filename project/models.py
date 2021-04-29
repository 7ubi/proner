from django.db import models
from django.conf import settings
from colorfield.fields import ColorField
from django.utils.text import slugify

# Create your models here.

class Project(models.Model):
    name = models.CharField(max_length=100)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        s = slugify(self.name)

        slugExists = Project.objects.filter(slug=s).exists()

        n = 1
        while slugExists:
            s = slugify(self.name + str(n))
            slugExists = Project.objects.filter(slug=s).exists()
            n += 1

        self.slug = s
        super().save(*args, **kwargs)

class Note(models.Model):
    name = models.CharField(max_length=100)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)
    text = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)



