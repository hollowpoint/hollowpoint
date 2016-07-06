from settings import *
import os

# These should really just be settings but for now it's ok.
os.environ['TRIGGER_HOST'] = '10.16.2.149'  # ess-jay-dee-net-mon-one
os.environ['TRIGGER_PORT'] = '9000'
os.environ['TRIGGER_SETTINGS'] = '/home/jathan/.trigger/settings.py'

# Used in hpt/supervisord.conf. Not currently in use.
# SERVER_IP = '192.168.33.10'
SERVER_IP = 'localhost'
