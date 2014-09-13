from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.fields import (ModificationDateTimeField,
                                         CreationDateTimeField)

from core.models import TaskState, TaskMeta

def _prototype_netdevices(netdevices_file):
    """
    Load NetDevices data from prototype file to use it as columns.gq$

    :param netdevices_file:
        A NetDevices.json file
    """
    import json
    with open(netdevices_file, 'r') as f:
        data = json.load(f)
    return data[0].keys()

# Create your models here.
_ndfile = '/home/jathan/sandbox/hollowpoint/configs/netdevices.json'

ADMIN_STATUS_CHOICES = (
    ('PRODUCTION', 'Production'),
    ('NON-PRODUCTION', 'Non-Production'),
)
OPERATION_STATUS_CHOICES = (
    ('MONITORED', 'Monitored'),
    ('NON-MONITORED', 'Non-Monitored'),
    ('IGNORED', 'Ignored'),
)
LIFECYCLE_STATUS_CHOICES = (
    ('INSTALLED', 'Installed'),
    ('DECOMMISSIONED', 'Decommissioned'),
    ('RMA', 'RMA'),
    ('STORAGE', 'Storage'),
)
AUTH_METHOD_CHOICES = (
    ('TACACS', 'TACACS+'),
    ('LOCAL', 'Local'),
    ('PASSWORD', 'Password'),
    ('SSH_KEY', 'SSH Public Key'),
    ('SNMP', 'SNMP'),
)
DEVICE_TYPE_CHOICES = (
    ('CONSOLE SERVER', 'Console Server'),
    ('FIREWALL', 'Firewall'),
    ('DWDM', 'Optical Wave'),
    ('LOAD BALANCING', 'Load-Balancer'),
    ('ROUTER', 'Router'),
    ('SWITCH', 'Switch'),
)
OOB_CONNECTOR_CHOICES = (
    ('SERIAL', 'Serial'),
    ('IPMI', 'IPMI'),
    ('ILO', 'ILO'),
)
VENDOR_CHOICES = (
    ('A10', 'A10 Networks'),
    ('ARISTA', 'Arista Networks'),
    ('ARUBA', 'Aruba Networks'),
    ('BROCADE', 'Brocade Communications Systems'),
    ('CISCO', 'Cisco Systems'),
    ('CITRIX', 'Citrix Systems'),
    ('DELL', 'Dell'),
    ('F5', 'F5 Networks'),
    ('FORCE10', 'Force10 Networks'),
    ('FOUNDRY', 'Foundry Networks'),
    ('JUNIPER', 'Juniper Networks'),
    ('MRV', 'MRV Communications'),
    ('NETSCREEN', 'NetScreen Technologies'),
    ('PALOALTO', 'Palo Alto Networks'),
)

def _get_netdevices():
    from trigger.netdevices import NetDevices
    nd = NetDevices()
    return nd

def make_asset_tag(fqdn):
    import uuid
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, str(fqdn)))

class NetDevice(models.Model):
    """
    Model for database models of NetDevice objects
    """
    # Basics
    #nodeName = models.CharField(max_length=255, default='', null=False, blank=True)
    node_name = models.CharField('Node Name', max_length=255, default='',
        null=False, blank=True, help_text='FQDN used to connect to the device')
    nodePort = models.CharField('Node Port', max_length=255, default='',
        null=False, blank=True, help_text=(
            'TCP port used to connect to the device. If not set, default of '
            '22/tcp is used.'))
    created = CreationDateTimeField('Created')
    modified = ModificationDateTimeField('Last Updated')
    #lastUpdate = modified

    # Status
    adminStatus = models.CharField(_('Administrative Status'), max_length=255,
        default='', null=False, blank=True, choices=ADMIN_STATUS_CHOICES,
        help_text='Administrative production status')
    lifecycleStatus = models.CharField('Lifecycle Status', max_length=255,
        default='', null=False, blank=True, choices=LIFECYCLE_STATUS_CHOICES,
        help_text='Device lifecycle status')
    operationStatus = models.CharField(_('Operation Status'), max_length=255,
        default='', null=False, blank=True, choices=OPERATION_STATUS_CHOICES,
        help_text='Operational monitoring status')

    # Administrivia
    assetID = models.CharField(_('Asset Tag'), max_length=255, default='',
        null=False, blank=True)
    barcode = models.CharField('Bar Code', max_length=255, default='',
        null=False, blank=True)
    budgetCode = models.CharField('Budget Code', max_length=255, default='',
        null=False, blank=True)
    budgetName = models.CharField('Budget Name', max_length=255, default='',
        null=False, blank=True)

    # Security
    authMethod = models.CharField(_('Authentication Method'), max_length=255,
        default='', null=False, blank=True, choices=AUTH_METHOD_CHOICES,
        help_text='Method of authentication used to login')
    loginPW = models.CharField('Login Password', max_length=255, default='',
        null=False, blank=True, help_text=(
            'VTY password used to login '
            '(Typically only on IOS-like devices)'))
    enablePW = models.CharField('Enable Password', max_length=255, default='',
        null=False, blank=True, help_text=(
            'Password used when entering enable mode '
            '(Typically only on IOS-like devices)'))

    #lastUpdate = models.CharField(max_length=255, default='', null=False, blank=True)
    #lastUpdate = ModificationDateTimeField('Last Update')
    layer2 = models.BooleanField('Supports Layer 2', default=True, null=False,
        blank=True)
    layer3 = models.BooleanField('Supports Layer 3', default=True, null=False,
        blank=True)
    layer4 = models.BooleanField('Supports Layer 4', default=True, null=False,
        blank=True)

    # Hardware info
    manufacturer = models.CharField(_('Vendor'), max_length=255, default='',
        null=False, blank=True, choices=VENDOR_CHOICES,
        help_text='Device manufacturer')
    deviceType = models.CharField('Device Type', max_length=255, default='',
        null=False, blank=True, choices=DEVICE_TYPE_CHOICES,
        help_text='Functional role this device serves')
    make = models.CharField(_('Make'), max_length=255, default='', null=False,
        blank=True, help_text='Make of the device')
    model = models.CharField(_('Model'), max_length=255, default='', null=False,
        blank=True, help_text='Model of the device')
    serialNumber = models.CharField('Serial Number', max_length=255, default='',
        null=False, blank=True)

    # On-call fields
    onCallEmail = models.EmailField(_('On-Call Email'), max_length=255,
        default='', null=False, blank=True)
    onCallID = models.CharField(_('On-Call ID'), max_length=255, default='',
        null=False, blank=True)
    onCallName = models.CharField(_('On-Call Group'), max_length=255,
        default='', null=False, blank=True)

    owner = models.CharField(_('Owner'), max_length=255, default='', null=False,
        blank=True)
    owningTeam = models.CharField(_('Owning Team'), max_length=255, default='',
        null=False, blank=True)
    projectName = models.CharField(_('Project Name'), max_length=255, default='',
        null=False, blank=True)

    # Location
    site = models.CharField('Site', max_length=255, default='', null=False,
        blank=True, help_text='Physical site location')
    room = models.CharField(_('Room'), max_length=255, default='',
        null=False, blank=True, help_text='Computer room')
    coordinate = models.CharField('Tile Coordinate', max_length=255, default='',
        null=False, blank=True)

    OOBTerminalServerConnector = models.CharField(_('Terminal Connector'),
        max_length=255, default='', null=False, blank=True,
        choices=OOB_CONNECTOR_CHOICES)
    OOBTerminalServerFQDN = models.CharField(_('Terminal Server'),
        max_length=255, default='', null=False, blank=True,
        help_text='FQDN of the terminal console server')
    OOBTerminalServerNodeName = models.CharField(_('Terminal Node Name'),
        max_length=255, default='', null=False, blank=True,
        help_text='Node name of the terminal server')
    OOBTerminalServerPort = models.CharField('Terminal Server Port', max_length=255,
        default='', null=False, blank=True,
        help_text='Terminal server port to which this device is connected')
    OOBTerminalServerTCPPort = models.CharField('TCP Port', max_length=255, default='',
        null=False, blank=True,
        help_text='TCP port used to connect to the console')

    tasks = models.ManyToManyField(TaskState, related_name='devices')

    @property
    def nodeName(self):
        return self.node_name

    def __unicode__(self):
        #return u'%s' % (self.nodeName,)
        return u'%s' % (self.node_name,)

    class Meta:
        verbose_name = _('Network Device')
        verbose_name_plural = _('Network Devices')
        ordering = ('node_name',)

    def get_tasks(self):
        #return '\n'.join(str(t) for t in self.tasks.all())
        ret = '<table>'

    get_tasks.short_description = 'Tasks'

    def get_acls(self):
        #return '\n'.join(str(t) for t in self.acls.all())
        ret = ''
        for acl in self.acls.all():
            tpl = '<a href="/acls/accesslist/%s/update/">%s</a><br>\n'
            row = tpl % (acl.id, acl.filename)
            ret += row
        return ret
    get_acls.allow_tags = True
    get_acls.short_description = 'Access-Lists'

    def get_acl_dict(self):
        if not hasattr(self, '_acl_dict'):
            self._acl_dict = {}
            try:
                from trigger.acl.db import AclsDB
            except ImportError:
                pass
            else:
                aclsdb = AclsDB()
                dev = _get_netdevices().get(self.nodeName)
                if dev is not None:
                    acl_dict = aclsdb.get_acl_dict(dev)
                    self._acl_dict = acl_dict

        return self._acl_dict

    @property
    def vendor(self):
        from trigger.netdevices import Vendor
        return Vendor(self.manufacturer)
    #vendor.short_description = 'Vendor'
    #vendor.is_column = True
