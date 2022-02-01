# Generated by Django 4.0.1 on 2022-02-01 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_remove_task_date_created_task_created_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='created_date',
        ),
        migrations.AddField(
            model_name='task',
            name='date_created',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
