from django.contrib import admin
from djcelery.models import TaskMeta

# Register your models here.

class TaskMetaAdmin(admin.ModelAdmin):
    """Celery TaskMeta information class"""
    readonly_fields = ('result',)
    search_fields = ('task_id',)
admin.site.register(TaskMeta, TaskMetaAdmin)
