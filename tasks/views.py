from multiprocessing import context
from django.shortcuts import render, redirect
from django.http import HttpResponse

# import the Task model
from .models import Task, CompletedTask

# Create your views here.
def index(request):
    return redirect('tasks')
# Add a new task
def add_task(request):
    # get the task as parameter
    task = request.GET.get('task')
    # create a new task
    new_task = Task(task=task)
    # save the task
    new_task.save()
    # redirect to the tasks view
    return redirect('tasks')

# Delete a task
def delete_task(request, task_id):
    # get the task as parameter
    task = [task for task in Task.objects.all()][task_id-1]
    # delete the task
    task.delete()
    # redirect to the tasks view
    return redirect('tasks')

# Complete a task
def complete_task(request, task_id):
    # get the task as parameter
    task = [task for task in Task.objects.all()][task_id-1]
    # create a new task
    new_task = CompletedTask(task=task)
    # save the task
    new_task.save()
    # delete the task
    task.delete()
    # redirect to the tasks view
    return redirect('tasks')

# View all tasks
def tasks(request):
    # get all tasks
    tasks = Task.objects.all()
    # render the tasks
    return render(request, 'tasks.html', {'tasks': tasks})

# View all completed tasks
def completed_tasks(request):
    # get all completed tasks
    completed_tasks = CompletedTask.objects.all()
    # render the completed tasks
    return render(request, 'completed_tasks.html', {'tasks': completed_tasks})

# delete  completed task
def delete_completed_task(request, task_id):
    # get the task as parameter
    task = [task for task in CompletedTask.objects.all()][task_id-1]
    # delete the task
    task.delete()
    # redirect to the tasks view
    return redirect('completed-tasks')

# view all tasks and completed tasks
def all_tasks(request):
    # get all tasks
    tasks = Task.objects.all()
    # get all completed tasks
    completed_tasks = CompletedTask.objects.all()
    # render the tasks and completed tasks
    return render(request, 'all_tasks.html', {'tasks': tasks, 'completed_tasks': completed_tasks})