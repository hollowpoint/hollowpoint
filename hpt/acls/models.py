from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.fields import (ModificationDateTimeField,
                                         CreationDateTimeField)

from inventory.models import NetDevice
#from core.models import TaskState, TaskMeta

# Used by AccessList model
FORMAT_CHOICES = (
    ('ios', 'Cisco IOS'),
    ('ios_named', 'Cisco IOS Named'),
    ('iosxr', 'Cisco IOS XR'),
    ('ios_brocade', 'Brocade'),
    ('junos', 'Juniper Packet Filter'),
)

class AccessList(models.Model):
    """
    Model for database models of ACL objects
    """
    filename = models.CharField(max_length=255, unique=True,
        help_text='Filename containing the policy contents')
    devices = models.ManyToManyField(NetDevice, related_name='acls', blank=True,
        help_text='Devices to which this access-list should be applied')
    format = models.CharField(choices=FORMAT_CHOICES, max_length=32,
        help_text='Vendor-specific format')

    created = CreationDateTimeField('Created')
    modified = ModificationDateTimeField('Modified')

    #tasks = models.ManyToManyField(TaskState, related_name='devices')

    def __unicode__(self):
        #return u'%s' % (self.nodeName,)
        return u'%s' % (self.filename,)

    class Meta:
        verbose_name = _('Access-List')
        verbose_name_plural = _('Access-Lists')
        ordering = ('filename',)

    def get_device_count(self):
        return self.devices.count()
    get_device_count.short_desccription = 'Device Count'

    def get_devices(self):
        return '\n'.join(str(t) for t in self.devices.all())
    get_devices.short_description = 'Network Devices'
