from django.db import models

#  create a model to store completed tasks
class CompletedTask(models.Model):
    # create a array field to store new task
    task = models.CharField(max_length=50)
    
    def __str__(self):
        return self.task

# create a model to store new tasks
class Task(models.Model):
    # create a array field to store new task
    task = models.CharField(max_length=50)
    
    def __str__(self):
        return self.task