from django.db import models
from django.contrib.auth import get_user_model
from djcelery.models import TaskMeta, TaskState

# Create your models here.
#User = get_user_model()

"""
class Task(models.Model):
    user = models.ForeignKey(User)
    executed = models.DateTimeField() # NYI
"""
