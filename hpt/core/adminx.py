import xadmin
from xadmin import views
from xadmin import layout
from xadmin.layout import (Main, TabHolder, Tab, Fieldset, Row, Col,
                           AppendedText, Side)
from xadmin.plugins.inline import Inline
from xadmin.plugins.batch import BatchChangeAction

from django.conf import settings
from celery import states
from django.utils.translation import ugettext_lazy as _
from django.utils.html import escape
from djcelery.admin_utils import action, display_field, fixedwidth
from djcelery.admin import colored_state

# Models
from inventory.models import NetDevice
from djcelery.models import TaskMeta, TaskState
from djcelery.admin import TaskMonitor

class MainDashboard(object):
    widgets = [
        [
            {
                'type': 'html',
                'title': 'Greetings',
                'content': 
                    """
                    <h3>Welcome to Hollowpoint!</h3>
                    <p>Join us on IRC at <a
                    href="irc://irc.freenode.net:6667/hollowpoint">#hollowpoint</b>
                    on Freenode.</p>
                    """
            },
            {
                'type': 'list',
                'model': 'inventory.netdevice',
                'params': {
                    'o': '-modified',
                }
            },
            {
                'type': 'list',
                'model': 'djcelery.taskmeta',
                'params': {
                    'o': '-date_done'
                }
            },
        ],
        [
            {
                'type': 'qbutton',
                'title': 'Quick Start',
                'btns': [
                    {
                        'model': 'inventory.netdevice',
                        'title': 'Devices',
                    },
                    {
                        'model': 'djcelery.taskstate',
                        'title': 'Tasks',
                    },
                ],
            },
        ],
    ]
xadmin.site.register(views.website.IndexView, MainDashboard)

class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True
xadmin.site.register(views.BaseAdminView, BaseSetting)

class GlobalSetting(object):
    site_title = settings.XADMIN_SITE_TITLE
    site_footer = settings.XADMIN_SITE_FOOTER
    global_search_models = [NetDevice, TaskMeta]
    global_models_icon = {
        NetDevice: 'fa fa-laptop',
        TaskMeta: 'fa fa-cloud',
    }
    menu_style = 'default' # 'accordion'
xadmin.site.register(views.CommAdminView, GlobalSetting)


# Gonna have to recreate the django-celery TaskState admin from scratch to work
# with xadmin. Let's make sure this is worth it before we do this!!
#class TaskStateAdmin(TaskMonitor):
TASK_STATE_COLORS = {states.SUCCESS: 'green',
                     states.FAILURE: 'red',
                     states.REVOKED: 'magenta',
                     states.STARTED: 'yellow',
                     states.RETRY: 'orange',
                     'RECEIVED': 'blue'}

import json
class TaskStateAdmin(object):
    list_filter = ('state', 'name', 'tstamp', 'eta', 'worker')
    list_display = ('task_id', 'state', 'name', 'args', 'kwargs', 'eta', 'tstamp', 'worker')
    #list_display = TaskMonitor.list_display
    search_fields = ('name', 'task_id', 'args', 'kwargs', 'worker__hostname')

    '''
    data_charts = {
        'task_count': {
            'title': 'Task Count',
            'x-field': 'state',
            'y-field': '
    }
    '''
xadmin.site.register(TaskState, TaskStateAdmin)

class TaskMetaAdmin(object):
    """Celery TaskMeta information class"""
    #readonly_fields = ('task_id', 'status', 'result', 'traceback')
    readonly_fields = ('task_id', 'status', 'traceback', 'get_result')
    exclude = ('result',)
    search_fields = ('task_id',)
    list_display = ('task_id', 'status', 'date_done', 'hidden')

    def get_result(self, obj):
        dumped = '<pre style="font-size: 11px">' + json.dumps(obj.result, indent=4) + '</pre>'
        return dumped
    get_result.allow_tags = True
    get_result.short_description = 'result'

    form_layout = (
        Main(
            'task_id',
            'status',
            'get_result',
            'traceback'
        ),
    )

xadmin.site.register(TaskMeta, TaskMetaAdmin)
