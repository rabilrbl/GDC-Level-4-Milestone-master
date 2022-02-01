from django.contrib import admin
from django.urls import path

from tasks.views import index, delete_task, complete_task
from tasks.views import GenericListView, delete_completed_task
from tasks.views import CreateTaskView, EditTaskView, GenericAllTaskView, GenericCompletedListView

urlpatterns = [
    path("admin/", admin.site.urls),
    # Add all your views here
    path("", index, name="index"),
    path("add-task/", CreateTaskView.as_view(), name="add-task"),
    path("create-task/", CreateTaskView.as_view(), name="create-task"),
    path("edit-task/<int:pk>/", EditTaskView.as_view(), name="edit-task"),
    path("delete-task/<int:task_id>/", delete_task, name="delete-task"),
    path("complete_task/<int:task_id>/", complete_task, name="complete-task"),
    path("tasks/", GenericListView.as_view(), name="tasks"),
    path("completed_tasks/", GenericCompletedListView.as_view(), name="completed-tasks"),
    path("delete-completed-task/<int:task_id>/", delete_completed_task, name="delete-completed-task"),
    path("all_tasks/", GenericAllTaskView.as_view(), name="all-tasks"),
]
