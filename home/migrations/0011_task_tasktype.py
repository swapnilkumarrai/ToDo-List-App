# Generated by Django 4.2.2 on 2023-08-13 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_task_taskpriority'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='taskType',
            field=models.CharField(default='Work', max_length=100),
            preserve_default=False,
        ),
    ]
