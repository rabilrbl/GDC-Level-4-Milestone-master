from django.contrib import admin
from django.urls import path

from tasks.views import index, add_task, delete_task, complete_task, tasks, completed_tasks, delete_completed_task, all_tasks

urlpatterns = [
    path("admin/", admin.site.urls),
    # Add all your views here
    path("", index, name="index"),
    path("add-task/", add_task, name="add-task"),
    path("delete-task/<int:task_id>/", delete_task, name="delete-task"),
    path("complete_task/<int:task_id>/", complete_task, name="complete-task"),
    path("tasks/", tasks, name="tasks"),
    path("completed_tasks/", completed_tasks, name="completed-tasks"),
    path("delete-completed-task/<int:task_id>/", delete_completed_task, name="delete-completed-task"),
    path("all_tasks/", all_tasks, name="all-tasks"),
]
