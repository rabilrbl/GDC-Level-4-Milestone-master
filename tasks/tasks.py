
from datetime import datetime, time
from django.contrib.auth.models import User
from django.core.mail import send_mail
from tasks.models import Task, Report

from task_manager.celery import app

@app.task
def send_email_report(report) -> None:
    user = report.user
    task = Task.objects.filter(user=user, deleted=False)
    # print(f"Sending email reminder to {user.username}\n")
    pending_tasks = task.filter(status="pending").count()
    completed_tasks = task.filter(status="completed").count()
    in_progress_tasks = task.filter(status="in_progress").count()
    cancelled_tasks = task.filter(status="cancelled").count()
    email_content = f"Hi {user.username},\n\nYou have {pending_tasks} pending tasks, {completed_tasks} completed tasks, {in_progress_tasks} in progress tasks, {cancelled_tasks} cancelled tasks.\n\nRegards,\nTask Manager"
    send_mail("Task Manager Report", email_content, "tasks@gdctasks.com", [user.email])
    # print("Email sent to {}".format(user.email))

@app.task
def periodic_emailer():
    currentTime = datetime.now()
    # print("Checking time for user daily report......")
    reports = Report.objects.filter(time__range=(time(currentTime.hour,currentTime.minute,0), time(currentTime.hour,currentTime.minute,59)), consent=True)
    for rpt in reports:
        send_email_report(rpt)

app.conf.beat_schedule["send-daily-user-report"] = {
        'task':'tasks.tasks.periodic_emailer',
        'schedule': 60.0,
}