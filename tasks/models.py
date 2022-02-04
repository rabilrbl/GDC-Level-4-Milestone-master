from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    title = models.CharField(max_length=100)
    priority = models.IntegerField(default=0)
    description = models.TextField(max_length=500, blank=True)
    completed = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def soft_delete(self):
        self.deleted = True
        self.save()
