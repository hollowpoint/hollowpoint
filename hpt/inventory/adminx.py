import xadmin
from xadmin import views
from xadmin import layout
from xadmin.plugins.inline import Inline
from xadmin.plugins.batch import BatchChangeAction

# Models
from inventory.models import NetDevice

# Register your models here.
class NetDeviceAdmin(object):
    """Customizing the view of devices in the admin"""
    list_filter = ('manufacturer', 'deviceType', 'site')
    list_display = ('nodeName', 'manufacturer', 'deviceType', 'make', 'model',
        'adminStatus')
    list_editable = ('nodeName', 'manufacturer', 'deviceType', 'make', 'model',
        'adminStatus')
    search_fields = ('nodeName',)
    style_fields = {'system': 'radio-inline'}

    form_layout = (
        layout.Main(
            layout.TabHolder(
                layout.Tab('Primary Fields',
                    layout.Fieldset('Basics',
                        'nodeName', 'nodePort', 'lastUpdate',
                        description='Used to connect to the device',
                    ),
                    layout.Fieldset('Hardware Info',
                        'manufacturer', 'deviceType',
                        layout.Row('make', 'model'),
                        'serialNumber',
                    ),
                    layout.Fieldset('Location',
                        layout.Row('site', 'room', 'coordinate'),
                    ),
                ),
                layout.Tab('Administrivia',
                    layout.Fieldset('Asset Information',
                        'assetID', 'budgetCode', 'budgetName', 
                    ),
                    layout.Fieldset('Contact details',
                        'owner', 'owningTeam', 'onCallName', 'onCallEmail',
                    ),
                ),
            ),
        ),
        layout.Side(
            layout.Fieldset('Status data',
                'adminStatus', 'operationStatus', 'lifecycleStatus',
            ),
        ),

    )

    fieldsets = (
        ('Basics', {
            'fields': ('nodeName', 'nodePort'),
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
