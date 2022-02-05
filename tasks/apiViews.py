from dataclasses import field
from enum import Flag
from tasks.models import Task
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer

from rest_framework.viewsets import ModelViewSet

from rest_framework.permissions import IsAuthenticated

from .views import updatePriority

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name","last_name","username")

class TaskSerializer(ModelSerializer):

    user = UserSerializer(read_only=True)

    class Meta:
        model = Task
        fields = ["id", "title", "priority", "description", "completed", "user"]

class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user, deleted=False)
    
    def takeCareOfPriority(self):
        # increments priority on change to avoid same values
        priority = self.request.data.get("priority")
        completed = self.request.data.get("completed")
        # completed returns None hence we define bool value
        if completed is None: completed = False
        updatePriority(priority, completed, self.request)

    def perform_create(self, serializer):
        self.takeCareOfPriority()
        return serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        self.takeCareOfPriority()
        return serializer.save()


    def perform_destroy(self, instance):
        return instance.soft_delete()