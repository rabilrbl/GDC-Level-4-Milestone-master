def task_count(request):
    from tasks.models import Task
    if request.user.is_authenticated:
        return {
            'total_tasks': Task.objects.filter(user=request.user, deleted=False).count(),
            'completed_tasks': Task.objects.filter(user=request.user, deleted=False, completed=True).count()
        }
    else:
        return {
            'total_tasks': 0,
            'completed_tasks': 0
        }
