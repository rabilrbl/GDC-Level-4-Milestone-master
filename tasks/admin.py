from django.contrib import admin

# Register your models here.
from .models import Task, History
admin.site.register(Task)
admin.site.register(History)