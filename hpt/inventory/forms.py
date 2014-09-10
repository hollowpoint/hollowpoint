from django import forms

from core.models import TaskState
from models import NetDevice

class InlineTaskForm(forms.ModelForm):
    class Meta:
        model = TaskState
