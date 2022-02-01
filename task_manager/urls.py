from django.contrib import admin
from django.urls import path

from tasks.views import index, AddTaskView, delete_task, complete_task, GenericListView, completed_tasks, delete_completed_task, all_tasks

urlpatterns = [
    path("admin/", admin.site.urls),
    # Add all your views here
    path("", index, name="index"),
    path("add-task/", AddTaskView.as_view(), name="add-task"),
    path("delete-task/<int:task_id>/", delete_task, name="delete-task"),
    path("complete_task/<int:task_id>/", complete_task, name="complete-task"),
    path("tasks/", GenericListView.as_view(), name="tasks"),
    path("completed_tasks/", completed_tasks, name="completed-tasks"),
    path("delete-completed-task/<int:task_id>/", delete_completed_task, name="delete-completed-task"),
    path("all_tasks/", all_tasks, name="all-tasks"),
]
