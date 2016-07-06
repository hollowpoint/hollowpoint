from django.contrib import admin
from djcelery.models import TaskMeta, TaskState, TaskSetMeta

# Register your models here.

class TaskMetaAdmin(admin.ModelAdmin):
    """Celery TaskMeta information class"""
    readonly_fields = ('result',)
    search_fields = ('task_id',)
    list_display = ('task_id', 'status', 'hidden')
admin.site.register(TaskMeta, TaskMetaAdmin)
admin.site.register(TaskSetMeta)

"""
from xadmin import models as xmodels
admin.site.register(xmodels.Bookmark)
admin.site.register(xmodels.UserSettings)
admin.site.register(xmodels.UserWidget)
"""
