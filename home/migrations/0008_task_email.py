# Generated by Django 4.2.2 on 2023-07-09 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_rename_username_task_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='eMail',
            field=models.EmailField(default='kumarswapnil.215@gmail.com', max_length=100),
            preserve_default=False,
        ),
    ]
