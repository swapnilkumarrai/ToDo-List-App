from django.db import models

# Create your models here.
class Task(models.Model):
    taskId = models.AutoField(primary_key=True)
    taskTitle = models.CharField(max_length=30, blank=True, null=True)
    taskDesc = models.TextField(blank=True, null=True)
    time = models.DateTimeField(auto_now_add=True)
    taskStatus = models.IntegerField(default=0)

    def __str__(self):
        return self.taskTitle