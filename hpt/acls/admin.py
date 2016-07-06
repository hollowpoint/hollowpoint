from django.contrib import admin
from . import models

# Register your models here.
class AccessListAdmin(admin.ModelAdmin):
    """Customizing the view of devices in the admin"""
    list_filter = ('filename', 'format')
    list_display = ('filename', 'format', 'modified', 'get_device_count')
    #list_editable = ('node_name', 'manufacturer', 'deviceType', 'make', 'model',
    #    'adminStatus')
    search_fields = ('filename',)
    # style_fields = {'system': 'radio-inline'}
    # grid_layouts = ('table', 'thumbnails')
    readonly_fields = ('created', 'modified')

    """
    fieldsets = (
        ('Basics', {
            'fields': ('filename', 'format', 'created', 'modified'),
        }),
        ('Network Devices': { 'fields': ['devices'] }
        ),
    )
    """
admin.site.register(models.AccessList, AccessListAdmin)
