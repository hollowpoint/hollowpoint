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

def _get_netdevices():
    from trigger.netdevices import NetDevices
    nd = NetDevices()
    return nd

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
    #nodeName = models.CharField(max_length=255, default='', null=False, blank=True)
    node_name = models.CharField('Node Name', max_length=255, default='', null=False, blank=True)
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

    @property
    def nodeName(self):
        return self.node_name

    def __unicode__(self):
        #return u'%s' % (self.nodeName,)
        return u'%s' % (self.node_name,)

    class Meta:
        verbose_name = _('Network Device')
        verbose_name_plural = _('Network Devices')

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

    # ACLs
    def get_acls(self):
        return self.get_acl_dict().get('all', set())
    #get_acls.short_description = 'All ACLs associated to this device'
    get_acls.short_description = 'All ACLs'
    get_acls.is_column = False

    @property
    def acls(self):
        return self.get_acls()

    # Explicit ACLs
    def get_explicit_acls(self):
        return self.get_acl_dict().get('explicit', set())
    #get_explicit_acls.short_description = 'ACLs explicitly associated to this device'
    get_explicit_acls.short_description = 'Explicit ACLs'
    get_explicit_acls.is_column = False

    @property
    def explicit_acls(self):
        return self.get_explicit_acls()

    # Implicit ACLs
    def get_implicit_acls(self):
        return self.get_acl_dict().get('implicit', set())
    #get_implicit_acls.short_description = 'ACLs automatically associated to this device'
    get_implicit_acls.short_description = 'Auto ACLs'
    get_implicit_acls.is_column = False

    @property
    def implicit_acls(self):
        return self.get_implicit_acls()
