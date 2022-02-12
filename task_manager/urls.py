from django.contrib import admin
from django.urls import path

from tasks.views import (index,
                         GenericListView, CreateTaskView,
                         EditTaskView, GenericAllTaskView, GenericCompletedListView,
                         TaskDetailView, DeleteTaskView, SignUpView, LoginView, CompleteTaskView,
                         CreateTimeView
                         )

from django.contrib.auth.views import LogoutView
from django.views.generic.base import RedirectView

from tasks.apiViews import TaskViewSet, HistoryViewSet

from rest_framework_nested import routers
# import DefaultRouter
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'api/tasks', TaskViewSet, basename='tasks')
client_router = routers.NestedSimpleRouter(router, r'api/tasks', lookup='history')
client_router.register(r'history', HistoryViewSet, basename="history")


# Api views
urlpatterns = [
    path("admin/", admin.site.urls),

    # Browser based view
    path("", index, name="index"),
    path("add-task/", CreateTaskView.as_view(), name="add-task"),
    path("create-task/", CreateTaskView.as_view(), name="create-task"),
    path("edit-task/<slug>/", EditTaskView.as_view(), name="edit-task"),
    path("detail-view/<slug>/", TaskDetailView.as_view(), name="detail-view"),
    path("delete-task/<slug>/", DeleteTaskView.as_view(), name="delete-task"),
    path("complete-task/<slug>/",
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
    path("completed-tasks/", GenericCompletedListView.as_view(),
         name="completed-tasks"),
    path("all-tasks/", GenericAllTaskView.as_view(), name="all-tasks"),
    path("report/create", CreateTimeView.as_view(), name="report-create"),
] + router.urls + client_router.urls
