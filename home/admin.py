from django.contrib import admin
from home.models import Task

# Register your models here.

class TaskAdmin(admin.ModelAdmin):
    list_display = ['taskTitle', 'taskDesc', 'time']
    search_fields = ['taskTitle']
    list_per_page = 8

admin.site.register(Task, TaskAdmin)