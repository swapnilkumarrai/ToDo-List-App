from django.contrib import admin
from home.models import Task, Contact

# Register your models here.

class TaskAdmin(admin.ModelAdmin):
    list_display = ['taskTitle', 'taskDesc', 'time']
    search_fields = ['taskTitle']
    list_per_page = 8

# Register the Task model
admin.site.register(Task, TaskAdmin)

# Register the Contact model
admin.site.register(Contact)