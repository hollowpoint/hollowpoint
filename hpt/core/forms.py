
from django.conf import settings
from django import forms
from django.forms import ValidationError as FormValidationError

import json
import requests

class ChangePasswordForm(forms.Form):
    """
    Form for changing device passwords.
    """
    devices = forms.CharField(
        label='Devices',
        widget=forms.Textarea,
        help_text=(
            'Devices on which you would like to set the new password. '
            'One per line.'
        ),
    )
    new_password = forms.CharField(
        label='New Password',
        help_text=(
            'The new password you would like apply to these devices.'
        )
    )

    def clean_devices(self):
        """Convert devices into a list"""
        devices = self.cleaned_data.get('devices')
        try:
            devices = devices.splitlines()
        except (TypeError, AttributeError) as err:
            raise FormValidationError(str(err))
        else:
            return devices

    def save(self, commit=True):
        """
        Given valid devices, password, execute the task
        """
        #print 'SUCCESS'
        kwargs = self.cleaned_data
        data = dict(kwargs=kwargs)
        payload = json.dumps(data)
        url = 'http://ops.lab.hollow.pt:5555/api/task/async-apply/core.tasks.change_password'
        r = requests.post(url, data=payload)
        rdata = r.json()
        return rdata['task-id']

from inventory.models import NetDevice
class ShowClockForm(forms.Form):
    """
    Form for fetching the time on devices.
    """
    devices = forms.ModelChoiceField(
        label='Devices',
        queryset=NetDevice.objects.all(),
        #widget=forms.Textarea,
        help_text=(
            'Devices on which you would like to get the time. '
            'One per line.'
        ),
    )

    '''
    def clean_devices(self):
        """Convert devices into a list"""
        devices = self.cleaned_data.get('devices')
        try:
            devices = devices.splitlines()
        except (TypeError, AttributeError) as err:
            raise FormValidationError(str(err))
        else:
            return devices
    '''

    def save(self, commit=True):
        """
        Given valid devices, password, execute the task
        """
        #print 'SUCCESS'
        kwargs = self.cleaned_data
        data = dict(kwargs=kwargs)
        payload = json.dumps(data)
        url = 'http://ops.lab.hollow.pt:5555/api/task/async-apply/core.tasks.show_clock'
        r = requests.post(url, data=payload)
        rdata = r.json()
        return rdata['task-id']
