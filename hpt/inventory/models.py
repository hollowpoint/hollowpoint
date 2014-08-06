from django.db import models
from django.utils.translation import ugettext_lazy as _

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

ADMINSTATUS_CHOICES = (
    ('PRODUCTION', 'Production'),
    ('NON-PRODUCTION', 'Non-Production'),
)

class NetDevice(models.Model):
    """
    Model for database models of NetDevice objects
    """
    #_fields = _prototype_netdevices(_ndfile)
    adminStatus = models.CharField(_('Administrative Status'), max_length=255,
        default='', null=False, blank=True, choices=ADMINSTATUS_CHOICES)
    assetID = models.CharField(max_length=255, default='', null=False, blank=True)
    authMethod = models.CharField(max_length=255, default='', null=False, blank=True)
    barcode = models.CharField(max_length=255, default='', null=False, blank=True)
    budgetCode = models.CharField(max_length=255, default='', null=False, blank=True)
    budgetName = models.CharField(max_length=255, default='', null=False, blank=True)
    coordinate = models.CharField(max_length=255, default='', null=False, blank=True)
    deviceType = models.CharField(max_length=255, default='', null=False, blank=True)
    enablePW = models.CharField(max_length=255, default='', null=False, blank=True)
    lastUpdate = models.CharField(max_length=255, default='', null=False, blank=True)
    layer2 = models.CharField(max_length=255, default='', null=False, blank=True)
    layer3 = models.CharField(max_length=255, default='', null=False, blank=True)
    layer4 = models.CharField(max_length=255, default='', null=False, blank=True)
    lifecycleStatus = models.CharField(max_length=255, default='', null=False, blank=True)
    loginPW = models.CharField(max_length=255, default='', null=False, blank=True)
    make = models.CharField(max_length=255, default='', null=False, blank=True)
    manufacturer = models.CharField(_('Vendor'), max_length=255, default='', null=False, blank=True)
    model = models.CharField(max_length=255, default='', null=False, blank=True)
    nodeName = models.CharField(max_length=255, default='', null=False, blank=True)
    nodePort = models.CharField(max_length=255, default='', null=False, blank=True)
    onCallEmail = models.CharField(max_length=255, default='', null=False, blank=True)
    onCallID = models.CharField(max_length=255, default='', null=False, blank=True)
    onCallName = models.CharField(max_length=255, default='', null=False, blank=True)
    operationStatus = models.CharField(max_length=255, default='', null=False, blank=True)
    owner = models.CharField(max_length=255, default='', null=False, blank=True)
    owningTeam = models.CharField(max_length=255, default='', null=False, blank=True)
    projectName = models.CharField(max_length=255, default='', null=False, blank=True)
    room = models.CharField(max_length=255, default='', null=False, blank=True)
    serialNumber = models.CharField(max_length=255, default='', null=False, blank=True)
    site = models.CharField(max_length=255, default='', null=False, blank=True)
    OOBTerminalServerConnector = models.CharField(max_length=255, default='', null=False, blank=True)
    OOBTerminalServerFQDN = models.CharField(max_length=255, default='', null=False, blank=True)
    OOBTerminalServerNodeName = models.CharField(max_length=255, default='', null=False, blank=True)
    OOBTerminalServerPort = models.CharField(max_length=255, default='', null=False, blank=True)
    OOBTerminalServerTCPPort = models.CharField(max_length=255, default='', null=False, blank=True)

    def __unicode__(self):
        return u'%s' % (self.nodeName,)

    class Meta:
        verbose_name = _('Network Device')
        verbose_name_plural = _('Network Devices')
