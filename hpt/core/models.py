from django.db import models
from django.contrib.auth import get_user_model
from djcelery.models import TaskMeta, TaskState, WorkerState

# Create your models here.
#User = get_user_model()

"""
class Task(models.Model):
    user = models.ForeignKey(User)
    executed = models.DateTimeField() # NYI
"""


'''
class TaskEvent(TaskState):
    """Union of TaskMeta and TaskState data."""
    def __init__(self, *args, **kwargs):
        super(TaskEvent, self).__init__(*args, **kwargs)
        self._task_meta = TaskMeta.objects.get(task_id=self.task_id)

    class Meta:
        proxy = True

    # These are all the fields that can be found on the TaskMeta instance
    @property
    def date_done(self):
        return self._task_meta.date_done

    @property
    def full_result(self):
        return self._task_meta.result

    @property
    def hidden(self):
        return self._task_meta.hidden
'''
