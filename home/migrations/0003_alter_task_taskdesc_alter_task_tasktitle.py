# Generated by Django 4.2.2 on 2023-06-10 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_remove_task_id_task_taskid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='taskDesc',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='task',
            name='taskTitle',
            field=models.CharField(blank=True, default='', max_length=30),
        ),
    ]
