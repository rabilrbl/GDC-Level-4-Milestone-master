web: gunicorn task_manager.wsgi
worker: celery -A task_manager worker --beat -l info