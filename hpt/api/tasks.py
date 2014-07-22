from __future__ import absolute_import
from celery import current_task, shared_task, Task
from celery.utils.log import get_task_logger
import importlib
from trigger.conf import settings
import os
import sys
import xmlrpclib

log = get_task_logger(__name__)

@shared_task
def add(x, y):
    return x + y

@shared_task
def mul(x, y):
    return x * y

@shared_task
def xsum(numbers):
    return sum(numbers)

@shared_task
def ping():
    return 'PONG'

TRIGGER_HOST = os.getenv('TRIGGER_HOST')
if TRIGGER_HOST is None:
    raise RuntimeError('You must define TRIGGER_HOST')
#XMLRPC_SERVER = xmlrpclib.Server('https://%s:9000/' % TRIGGER_HOST)
XMLRPC_SERVER = xmlrpclib.Server('http://%s:9000/' % TRIGGER_HOST)

# To save typing for SessionTask tasks
my = current_task

class SessionTask(Task):
    """
    Task base to be used for any task that will send credentials to Trigger.
    Use the ``creds`` attribute in your task functions like so::

        from celery import task, current_task as my

        @shard_task(base=SessionTask)
        def do_stuff(api_key):
            return my.creds

    Creds expects to find the ``api_key`` within the task's ``kwargs``.
    """
    abstract = True

    @property
    def creds(self):
        """
        api_key = self.request.kwargs.get('api_key')
        a = ApiKey.objects.get(key=api_key)
        creds = {'username': a.user.username,
             'password': a.password,
             'realm': 'hpt'}
        """
        creds = {
            'username': 'admin',
            'password': '00bliss!',
            'realm': 'hpt',
        }
        return creds
        #xxx return self._get_session(session_key)

    @property
    def method_name(self):
        """
        Return the method_name to map to based on ``current_task.name``.

        e.g. "api.tasks.execute_commands" returns "execute_commands"
        """
        _, method_name = self.name.rsplit('.', 1)
        return method_name


def load_plugin_tasks(force=False):
    """Load all task plugins listed in `~trigger.conf.settings`"""
    # Combine built-in and Commando plugins into a single set
    all_plugins = set(settings.BUILTIN_PLUGINS + settings.COMMANDO_PLUGINS)
    for mod_name in all_plugins:
        _load_plugin_task(mod_name, force=force)

def _load_plugin_task(mod_name, force=False):
    """Load a single task dynamically"""
    module = None
    if mod_name in sys.modules:
        # Check if module is already loaded
        if force:
            # Allow user to force reload of module
            module = reload(sys.modules[mod_name])
        else:
            # If not forcing reload, don't bother with the rest
            return None
    else:
        try:
            module = importlib.import_module(mod_name, __name__)
        except:
            pass

    if not module:
        log.warn("    Unable to load module: " + mod_name)
        return None

    # This will create the dynamic task. We're assuming the queue will be
    # 'api.tasks.' for now. This will likely have to be adapted somehow in the
    # future for more complex environments. Perhaps in the task plugin?
    task_name = module.task_name
    @shared_task(base=SessionTask, name='api.tasks.' + task_name)
    def dummy(devices, *args, **kwargs):
    #def dummy(devices, api_key, *args, **kwargs):
        return run(my.method_name, creds=my.creds, devices=devices, *args, **kwargs)

    XMLRPC_SERVER.add_handler(mod_name, task_name, force)

def run(method, *args, **kwargs):
    """Calls the ``method`` on the XMLRPC server."""
    log.warn('run> method: %r' % method)

    # Do this to obfuscate the password if creds were passed as an arg
    args_ = args[1:]
    log.warn('run>   args: %r' % (args_,))

    # Dot his to obfuscate the password if creds were passed as a kwarg
    kwargs_ = kwargs.copy()
    if 'creds' in kwargs_:
        kwargs_['creds'] = kwargs_['creds'].copy()
        kwargs_['creds']['password'] = '########'
    log.warn('run> kwargs: %r' % kwargs_)

    # Execute and return the result
    job = getattr(XMLRPC_SERVER, method)
    result = job(args, kwargs)
    return result

##
## Built-in tasks. In the future all built-in tasks will be plugins!
## (In Soviet Russia, task plugs you!)
##
@shared_task(base=SessionTask)
def execute_commands(devices, commands, force_cli=False, *args, **kwargs):
#def execute_commands(devices, commands, api_key, force_cli=False, *args, **kwargs):
    return run(my.method_name, creds=my.creds, devices=devices, commands=commands, force_cli=force_cli, *args, **kwargs)

"""
@shared_task
def execute_commands(*args, **kwargs):
    result = XMLRPC_SERVER.execute_commands(args, kwargs)
    return result
"""

@shared_task
def trigger_add(x, y):
    result = XMLRPC_SERVER.add(x, y)
    return result

# Load the pluggable tasks
load_plugin_tasks()
