import time

from django.contrib.auth.models import User
from django.core.mail import send_mail
from tasks.models import Task
from datetime import timedelta

from celery.decorators import periodic_task

from task_manager.celery import app

@periodic_task(run_every=timedelta(seconds=10))
def send_email_reminder():
    print("Sending email reminder")
    for user in User.objects.all():
        pending_tasks = Task.objects.filter(user=user, status="pending").count()
        completed_tasks = Task.objects.filter(user=user, status="completed").count()
        in_progress_tasks = Task.objects.filter(user=user, status="in_progress").count()
        cancelled_tasks = Task.objects.filter(user=user, status="cancelled").count()
        email_content = "Hi {},\n\nYou have {} pending tasks, {} completed tasks, {} in progress tasks and {} cancelled tasks.\n\nRegards,\nTask Manager".format(user.username, pending_tasks, completed_tasks, in_progress_tasks, cancelled_tasks)
        send_mail("Task Manager Report", email_content, "tasks@gdctasks.com", [user.email])
        print("Email sent to {}".format(user.email))