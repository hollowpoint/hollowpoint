import xadmin
from xadmin import views
from xadmin import layout
from xadmin.layout import (Main, TabHolder, Tab, Fieldset, Row, Col,
                           AppendedText, Side)
from xadmin.plugins.inline import Inline
from xadmin.plugins.batch import BatchChangeAction
from xadmin.views.list import FakeMethodField

# Models
from inventory.models import NetDevice

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
    readonly_fields = ('get_acls', 'get_explicit_acls', 'get_implicit_acls')

    form_layout = (
        Main(
            TabHolder(
                Tab('Primary Fields',
                    Fieldset('Basics',
                        'node_name', 'nodePort', 'lastUpdate',
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
                        'assetID', 'budgetCode', 'budgetName',
                    ),
                    Fieldset('Contact details',
                        'owner', 'owningTeam', 'onCallName', 'onCallEmail',
                    ),
                ),
                Tab('Security',
                    Fieldset('Access-Lists',
                        'get_acls',
                        'get_explicit_acls',
                        'get_implicit_acls',
                        description='ACLs and security policies',
                    ),
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
