from django.contrib import admin
import xadmin
from xadmin import views
from xadmin import layout
from xadmin.layout import (Main, TabHolder, Tab, Fieldset, Row, Col,
                           AppendedText, Side)
from xadmin.plugins.inline import Inline
from xadmin.plugins.batch import BatchChangeAction
#from xadmin.views.list import FakeMethodField

# Models
from inventory.models import NetDevice
from core.models import TaskState


class ReadonlyTabularInline(admin.TabularInline):
    """
    Credit: https://djangosnippets.org/snippets/2629/
    """
    can_delete = False
    extra = 0
    editable_fields = []

    def get_readonly_fields(self, request, obj=None):
        fields = []
        for field in self.model._meta.get_all_field_names():
            if (not field == 'id'):
                if (field not in self.editable_fields) and (field not in self.exclude):
                    fields.append(field)
        return fields

    def has_add_permission(self, request):
        return False

# Register your models here.
class NetDeviceAdmin(object):
    """Customizing the view of devices in the admin"""
    list_filter = ('manufacturer', 'deviceType', 'site')
    list_display = ('node_name', 'manufacturer', 'deviceType', 'make', 'model',
        'adminStatus')
    list_editable = ('node_name', 'manufacturer', 'deviceType', 'make', 'model',
        'adminStatus')
    search_fields = ('node_name',)
    style_fields = {'system': 'radio-inline'}
    grid_layouts = ('table', 'thumbnails')
    readonly_fields = ('get_acls', 'get_explicit_acls', 'get_implicit_acls',
        'get_tasks', 'modified')
    exclude = ('tasks',)

    form_layout = (
        Main(
            TabHolder(
                Tab('Primary Fields',
                    Fieldset('Basics',
                        'node_name', 'nodePort', 'modified',
                        description='Used to connect to the device',
                    ),
                    Fieldset('Hardware Info',
                        'manufacturer', 'deviceType', 'make', 'model',
                        'serialNumber',
                    ),
                    Fieldset('Location',
                        'site', 'room', 'coordinate',
                    ),
                ),
                Tab('Administrivia',
                    Fieldset('Asset Information',
                        'assetID', 'barcode', 'budgetCode', 'budgetName',
                        'projectName',
                    ),
                    Fieldset('Contact details',
                        'owner', 'owningTeam', 'onCallName', 'onCallEmail',
                        'onCallID',
                    ),
                ),
                Tab('Security',
                    Fieldset('Authentication',
                        'authMethod', 'enablePW', 'loginPW',
                    ),
                    Fieldset('Access-Lists',
                        'get_acls',
                        'get_explicit_acls',
                        'get_implicit_acls',
                        description='ACLs and security policies',
                    ),
                ),
                Tab('Network',
                    Fieldset('Out-of-Band',
                        'OOBTerminalServerConnector', 'OOBTerminalServerFQDN',
                        'OOBTerminalServerNodeName', 'OOBTerminalServerPort',
                        'OOBTerminalServerTCPPort',
                        description='Out-of-band console information',
                    ),
                    Fieldset('Features',
                        'layer2', 'layer3', 'layer4',
                    ),
                ),
                Tab('Tasks',
                    'get_tasks',
                    description='Task results',
                ),
            ),
        ),
        Side(
            Fieldset('Status data',
                'adminStatus', 'operationStatus', 'lifecycleStatus',
            ),
        ),

    )

    reversion_enabled = True

    """
    fieldsets = (
        ('Basics', {
            'fields': ('node_name', 'nodePort'),
        }),
        ('Hardware Info', {
            'fields': ('manufacturer', 'deviceType', 'make', 'model', 'serialNumber')
        }),
        ('Administrivia', {
            'fields': (
                'adminStatus', 'assetID', 'budgetCode', 'budgetName',
                'enablePW', 'owningTeam', 'owner', 'onCallName',
                'operationStatus', 'lastUpdate', 'lifecycleStatus',
                'projectName'),
        }),
        ('Location', {
            'fields': ('site', 'room', 'coordinate'),
        }),
    )
    """

    data_charts = {
        'devices_by_vendor': {
            'title': 'Devices by Vendor',
            'x-field': 'manufacturer',
            'y-field': ('manufacturer',),
            'option': {
                'series':{'bars': {'align': 'center', 'barWidth': 0.8, 'show': True}},
                'xaxis': {'aggregate': 'count', 'mode': 'categories'},
            },
        }
    }

xadmin.site.register(NetDevice, NetDeviceAdmin)
