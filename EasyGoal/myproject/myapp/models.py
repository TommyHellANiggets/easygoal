# models.py
from django.db import models
from django.utils import timezone

class Task(models.Model):
    description = models.TextField()
    category = models.CharField(max_length=255, blank=True, null=True)
    due_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.description

from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


