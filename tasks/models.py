from django.db import models

class Task(models.Model):
    priority = models.IntegerField(default=0)
    title = models.CharField(max_length=100)
    # description = models.TextField()
    completed = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title