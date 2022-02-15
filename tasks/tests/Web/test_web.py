from urllib import response
from django.contrib.auth.models import User, AnonymousUser

from tasks.models import Task, History, Report

from django.test import TestCase, RequestFactory, Client

from django.http.response import Http404

# Web View
from tasks.views import (
    GenericListView, CreateTaskView, 
    EditTaskView, TaskDetailView, 
    DeleteTaskView, CompleteTaskView,
    LoginView, SignUpView,

    GenericCompletedListView, GenericAllTaskView
)

# Api Views
from tasks.views import (
    GenericListView,
)

class WebAuthTests(TestCase):

    def test_not_authenticated(self):
        """
        Try to GET the tasks listing page, expect the response to redirect to the login page
        """
        authenticated_endpoints = [
            'tasks',
            'add-task',
            'completed-tasks',
            'all-tasks',
            'reports',
            'create-task',
            'edit-task/1',
            'detail-view/1',
            'delete-task/1',
            'complete-task/1',
        ]

        redirect_url = "/user/login/?next="

        for uri in authenticated_endpoints:
            uri = f"/{uri}/"
            response = self.client.get(uri)
            self.assertRedirects(response, redirect_url+uri)

        non_auth_uris = [

            '/user/login/',
            '/user/signup/',
        ]
        for uri in non_auth_uris:
            response = self.client.get(uri)
            self.assertEqual(response.status_code, 200)

class WebAuthorizedTests(TestCase):
    def setUp(self) -> None:
        """Initialize"""
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username="bruce_wayne", email="bruce@wayne.org", password="i_am_batman")
        # Create an instance of a GET request.
        self.request = self.factory.get("/")
        # Set the user instance on the request.
        self.request.user = self.user

        self.task1 = Task.objects.create(priority=1,title="This is a long test task name", description="test description", user=self.user)

        self.user2 = User.objects.create_user(username="authtest", email="authtest@test.in", password="authtestsecret")
        self.task2 = Task.objects.create(priority=2, title="This is a second task name", description="test description", user=self.user2)


    def test_login_view(self):
        """
        Test Login Page components
        """
        request = self.factory.get("/user/login/")
        request.user = AnonymousUser()
        response = LoginView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        response_content = response.render().content.decode()
        self.assertInHTML("Login", response_content)
        self.assertInHTML("Username", response_content, 1)
        self.assertInHTML("Password", response_content, 1)

    def test_signup_view(self):
        """
        Test Signup Page components
        """
        request = self.factory.get("/user/signup/")
        request.user = AnonymousUser()
        response = SignUpView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        response_content = response.render().content.decode()
        self.assertInHTML("Name", response_content)
        self.assertInHTML("Username", response_content)
        self.assertInHTML("Email", response_content)
        self.assertInHTML("Password", response_content)
        self.assertInHTML("Confirm Password", response_content)
        self.assertInHTML("terms and conditions", response_content)

    
    def test_generic_view_components(self):
        """
        Check generic view components
        """
        response = GenericListView.as_view()(self.request)
        self.assertEqual(response.status_code, 200)

        response = GenericCompletedListView.as_view()(self.request)
        self.assertEqual(response.status_code, 200)

        response = GenericAllTaskView.as_view()(self.request)
        self.assertEqual(response.status_code, 200)

    def test_create_task_view(self):
        """
        Test Create Task View
        """
        response = CreateTaskView.as_view()(self.request)
        self.assertEqual(response.status_code, 200)
        response_content = response.render().content.decode()
        self.assertInHTML("Title", response_content)
        self.assertInHTML("Priority", response_content)
        self.assertInHTML("Description", response_content)
        self.assertInHTML("Status", response_content)
    
    def test_edit_task_view(self):
        """
        Test Edit Task View
        """
        response = EditTaskView.as_view()(self.request, pk=self.task1.pk)
        self.assertEqual(response.status_code, 200)
        response_content = response.render().content.decode()
        self.assertIn(self.task1.title, response_content)
        self.assertInHTML(self.task1.description, response_content)

    def test_detail_view(self):
        """
        Test Detail Task View
        """
        response = TaskDetailView.as_view()(self.request, pk=self.task1.pk)
        self.assertEqual(response.status_code, 200)
        response_content = response.render().content.decode()
        self.assertInHTML(self.task1.title, response_content)
        self.assertInHTML(self.task1.description, response_content)

    def test_complete_view(self):
        """
        Test Mark Complete View
        """
        response = CompleteTaskView.as_view()(self.request, slug=self.task1.external_id)
        self.assertEqual(response.status_code, 302)

    def test_delete_view(self):
        """
        Test Delete Task Component
        """
        response = DeleteTaskView.as_view()(self.request, pk=self.task1.pk)
        self.assertEqual(response.status_code, 200)
        response_content = response.render().content.decode()
        self.assertInHTML(f'"{self.task1.title}"', response_content)
        self.assertInHTML("Delete", response_content)
        self.assertInHTML("Cancel", response_content)
    
    def test_soft_delete(self):
        """
        Test Soft Delete in views
        """
        # Test soft delete
        self.task1.deleted=True
        self.task1.save()

        self.assertRaises(Http404, TaskDetailView.as_view(), self.request, pk=self.task1.pk)
        self.assertRaises(Http404, EditTaskView.as_view(), self.request, pk=self.task1.pk)
        self.assertRaises(Http404, DeleteTaskView.as_view(), self.request, pk=self.task1.pk)

    def test_error_generic_view_components(self):
        """
        Random Tests
        """
        # unauthorized access
        self.assertRaises(Http404,  EditTaskView.as_view(), self.request, pk=self.task2.pk)
        self.assertRaises(Http404,  TaskDetailView.as_view(), self.request, pk=self.task2.pk)
        self.assertRaises(Http404, CompleteTaskView.as_view(), self.request, slug=self.task2.external_id)
        self.assertRaises(Http404,  DeleteTaskView.as_view(), self.request, pk=self.task2.pk)

        # random value test
        self.assertRaises(Http404, TaskDetailView.as_view(), self.request, pk=99)
        self.assertRaises(Http404, EditTaskView.as_view(), self.request, pk=101)
        self.assertRaises(Http404, DeleteTaskView.as_view(), self.request, pk=13)



# class ApiTestViews(TestCase):


    
        




    