from django.contrib import admin
from djcelery.models import TaskMeta, TaskState

# Register your models here.

class TaskMetaAdmin(admin.ModelAdmin):
    """Celery TaskMeta information class"""
    readonly_fields = ('result',)
    search_fields = ('task_id',)
    list_display = ('task_id', 'status', 'hidden')
admin.site.register(TaskMeta, TaskMetaAdmin)
