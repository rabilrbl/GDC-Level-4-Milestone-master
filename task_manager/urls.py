from django.contrib import admin
from django.urls import path

from tasks.views import (index,
                         GenericListView, CreateTaskView,
                         EditTaskView, GenericAllTaskView, GenericCompletedListView,
                         TaskDetailView, DeleteTaskView, SignUpView, LoginView, CompleteTaskView
                         )

from django.contrib.auth.views import LogoutView
from django.views.generic.base import RedirectView


urlpatterns = [
    path("admin/", admin.site.urls),
    # Add all your views here
    path("", index, name="index"),
    path("add-task/", CreateTaskView.as_view(), name="add-task"),
    path("create-task/", CreateTaskView.as_view(), name="create-task"),
    path("edit-task/<int:pk>/", EditTaskView.as_view(), name="edit-task"),
    path("detail-view/<int:pk>/", TaskDetailView.as_view(), name="detail-view"),
    path("delete-task/<int:pk>/", DeleteTaskView.as_view(), name="delete-task"),
    path("complete_task/<int:pk>/",
         CompleteTaskView.as_view(), name="complete-task"),
    path("tasks/", GenericListView.as_view(), name="tasks"),
    path("user/signup/", SignUpView.as_view(), name="signup"),
    path("user/login/", LoginView.as_view(), name="login"),
    path("user/logout/", LogoutView.as_view(), name="logout"),
    path("login/", RedirectView.as_view(url="/user/login/",
         permanent=True), name="login_redirect"),
    path("signup/", RedirectView.as_view(url="/user/signup/",
         permanent=True), name="signup_redirect"),
    path("logout/", RedirectView.as_view(url="/user/logout/",
         permanent=True), name="logout_redirect"),
    path("completed_tasks/", GenericCompletedListView.as_view(),
         name="completed-tasks"),
    path("all_tasks/", GenericAllTaskView.as_view(), name="all-tasks"),
]
