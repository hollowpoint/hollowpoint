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
from acls.models import AccessList


# Register your models here.
class AccessListAdmin(object):
    """Customizing the view of devices in the admin"""
    list_filter = ('filename', 'format')
    list_display = ('filename', 'format', 'modified', 'get_device_count')
    #list_editable = ('node_name', 'manufacturer', 'deviceType', 'make', 'model',
    #    'adminStatus')
    search_fields = ('filename',)
    style_fields = {'system': 'radio-inline'}
    grid_layouts = ('table', 'thumbnails')
    readonly_fields = ('created', 'modified')
    #exclude = ('acls',)

    form_layout = (
        Main(
            TabHolder(
                Tab('Primary Fields',
                    Fieldset('Basics',
                        'filename', 'format', 'created', 'modified',
                        description='ACL information',
                    ),
                ),
                Tab('Network Devices',
                    'devices',
                ),
            ),
        ),
        #Side(
        #    Fieldset('Status data',
        #        'adminStatus', 'operationStatus', 'lifecycleStatus',
        #    ),
        #),

    )

    reversion_enabled = True

    '''
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
    '''

xadmin.site.register(AccessList, AccessListAdmin)
