from re import search
from django.shortcuts import redirect, render

from django.views import View
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView

from django.forms import ModelForm, ValidationError
from django import forms
# import the Task model
from tasks.models import Task

# Create your views here.
def index(request):
    return redirect('tasks')

class TaskCreateForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'priority', 'description', 'completed']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'bg-gray-200 border border-gray-200 rounded-lg px-4 py-1 focus:ring-blue-500'}),
            'priority': forms.NumberInput(attrs={'class': 'bg-gray-200 border border-gray-200 rounded-lg px-4 py-1 focus:ring-blue-500'}),
            'description': forms.Textarea(attrs={'class': 'bg-gray-200 border border-gray-200 rounded-lg px-4 py-1 focus:ring-blue-500'}),
            'completed': forms.CheckboxInput(attrs={'class': 'bg-gray-200 rounded-xl px-4 py-1 focus:ring-blue-500 hover:ring-blue-500 h-4 w-4 bg-blue-500'}),
        }
    
    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) < 8:
            raise ValidationError("Task title must be at least 8 characters long.")
        return title.capitalize()
    
    def clean_priority(self):
        priority = self.cleaned_data['priority']
        exist_priority = Task.objects.filter(priority=priority, completed=False).exists()
        # if priority exists in the database
        if exist_priority:
            # increment the existing priority until it is unique
            new_priority = int(priority) + 1
            exist_priority = Task.objects.filter(priority=new_priority, completed=False).exists()
            while exist_priority:
                new_priority += 1
                exist_priority = Task.objects.filter(priority=new_priority, completed=False).exists()
            # save
            Task.objects.filter(priority=priority).update(priority=new_priority)
        return priority
        

class CreateTaskView(CreateView):
    form_class = TaskCreateForm
    template_name = 'create_task.html'
    success_url = '/tasks/'

class EditTaskView(UpdateView):
    model = Task
    form_class = TaskCreateForm
    template_name = 'edit_task.html'
    success_url = '/tasks/'

# class AddTaskView(View):
#     def get(self, request):
#         return redirect('create-task')
#     def post(self, request):
#         # get the task as parameter
#         task = request.POST.get('task')
#         priority = request.POST.get('priority')
#         # check if priority exists in the database
#         exist_priority = Task.objects.filter(priority=priority, completed=False).exists()
#         # if priority exists in the database
#         if exist_priority:
#             # increment the existing priority until it is unique
#             new_priority = int(priority) + 1
#             exist_priority = Task.objects.filter(priority=new_priority, completed=False).exists()
#             while exist_priority:
#                 new_priority += 1
#                 exist_priority = Task.objects.filter(priority=new_priority, completed=False).exists()
#             # save
#             Task.objects.filter(priority=priority).update(priority=new_priority)
#         # create a new task
#         new_task = Task(title=task, completed=False, priority=priority)
#         # save the task
#         new_task.save()
#         # redirect to page where task was added
#         return redirect('tasks')

# Delete a task
def delete_task(request, task_id):
    # get the task as parameter
    task = Task.objects.get(id=task_id)
    # delete the task
    task.delete()
    # redirect to the tasks view
    return redirect('tasks')

# Complete a task
def complete_task(request, task_id):
    # get the task as parameter
    task = Task.objects.get(id=task_id)
    task.completed = True
    # save the task
    task.save()
    # redirect to the tasks view
    return redirect('tasks')

# View all tasks

class GenericListView(ListView):
    template_name = 'tasks.html'
    context_object_name = 'tasks'
    paginate_by = 5

    def get_queryset(self):
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = Task.objects.filter(title__icontains=search_query, completed=False).order_by('priority')
        else:
            queryset = Task.objects.filter(completed=False).order_by('priority')
        return queryset

# View all completed tasks
class GenericCompletedListView(ListView):
    template_name = 'tasks.html'
    context_object_name = 'tasks'
    paginate_by = 5

    def get_queryset(self):
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = Task.objects.filter(title__icontains=search_query, completed=True).order_by('priority')
        else:
            queryset = Task.objects.filter(completed=True).order_by('priority')
        return queryset

# delete  completed task
def delete_completed_task(request, task_id):
    # get the task as parameter
    task = Task.objects.get(id=task_id)
    # delete the task
    task.delete()
    # redirect to the tasks view
    return redirect('completed-tasks')

# view all tasks and completed tasks
class GenericAllTaskView(ListView):
    template_name = 'tasks.html'
    context_object_name = 'tasks'
    paginate_by = 5

    def get_queryset(self):
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = Task.objects.filter(title__icontains=search_query).order_by('priority')
        else:
            queryset = Task.objects.all().order_by('priority')
        return queryset