from django.contrib import admin
from . import models

# Register your models here.
class NetDeviceAdmin(admin.ModelAdmin):
    """Customizing the view of devices in the admin"""
    list_display = ('nodeName', 'manufacturer', 'deviceType', 'make', 'model')
    list_filter = ('manufacturer', 'deviceType', 'site')
    search_fields = ('node_name',)
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
                'operationStatus', 'lifecycleStatus',
                'projectName'),
        }),
        ('Location', {
            'fields': ('site', 'room', 'coordinate'),
        }),
    )
admin.site.register(models.NetDevice, NetDeviceAdmin)
