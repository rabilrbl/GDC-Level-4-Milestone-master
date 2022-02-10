
from cProfile import label
from random import choices
from secrets import choice
from tasks.models import History, Task, STATUS_CHOICES
from django.contrib.auth.models import User

from rest_framework.serializers import ModelSerializer

from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from rest_framework.permissions import IsAuthenticated

from django_filters.rest_framework import DjangoFilterBackend, FilterSet, CharFilter, ChoiceFilter, DateTimeFilter



class FilterClass(FilterSet):
    title = CharFilter(lookup_expr="icontains")
    completed = ChoiceFilter(label="Completion",choices=((True,"Completed tasks"),(False,"Non-completed tasks")))
    status = ChoiceFilter(choices=STATUS_CHOICES)

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name","last_name","username")


class TaskSerializer(ModelSerializer):

    user = UserSerializer(read_only=True)
    status = ChoiceFilter(choices=STATUS_CHOICES)

    class Meta:
        model = Task
        fields = ["id", "title", "priority", "description", "date_created", "status", "user"]

class TaskViewSet(ModelViewSet):

    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    permission_classes = (IsAuthenticated,)

    filter_backends = (DjangoFilterBackend,)
    filterset_class = FilterClass


    def get_queryset(self):
        return Task.objects.filter(user=self.request.user, deleted=False)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        return instance.soft_delete()

class HistoryFilter(FilterSet):
    change_date = DateTimeFilter(label="Modified Date")

class HistorySerializer(ModelSerializer):
    task = TaskSerializer(read_only=True)
    class Meta:
        model = History
        fields = ["old_status", "new_status", "change_date","task"]

class HistoryViewSet(ReadOnlyModelViewSet):

    permission_classes = (IsAuthenticated,)

    filter_backends = (DjangoFilterBackend,)
    filterset_class = HistoryFilter
    serializer_class = HistorySerializer

    queryset = History.objects.all()

    def get_queryset(self):
        return History.objects.filter(user=self.request.user)
