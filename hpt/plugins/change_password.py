#!/usr/bin/env python -W ignore::DeprecationWarning
# -*- coding: utf-8 -*-

# change_password.py - Password Changer using CommandoApplication library

import collections
from functools import wraps
from twisted.python import log
#from trigger.cmds import Commando
from trigger.netdevices import NetDevices
from trigger.utils import crypt_md5
import xml.etree.cElementTree as ET

# Commando Plugin stuff
from trigger.utils import xmltodict, strip_juniper_namespace
from trigger.contrib.commando import CommandoApplication
import xml.etree.ElementTree as ET
from xml.etree.cElementTree import ElementTree, Element, SubElement

task_name = 'change_password'

# Namedtuple for use by command-emitting functions that return a 2-tuple of
# (cmds, status)
CommandsStatus = collections.namedtuple('CommandsStatus', 'cmds status')

def xmlrpc_change_password(*args, **kwargs):
    """XMLRPC method for Trigger daemon"""
    log.msg('Creating ChangePassword')
    log.msg('args = %s' % (args,))
    log.msg('kwargs = %s' % (kwargs,))
    cp = ChangePassword(*args, **kwargs)
    d = cp.run()
    return d

class ChangePassword(CommandoApplication):
    """
    Change passwords on network devices.

    ``work`` should be a dictionary of {'device_name': 'password', ...}
    """
    def __init__(self, devices, new_password, *args, **kwargs):
        #self.work = work
        self.new_password = new_password
        self.failures = {}
        self.production_only = kwargs.get('production_only', True)
        self.nd = NetDevices(with_acls=False, production_only=self.production_only)
        self._super = super(ChangePassword , self)
        #devices = self.work.keys()
        self._super.__init__(devices=devices, *args, **kwargs)

    def errback(self, reason, dev):
        """Catch the error and store the result."""
        self._super.errback(reason, dev)
        #self.failures[dev] = reason
        log.msg('FAILURE: %s' % device)

    def ioslike(self, generate):
        """
        Decorator to wrap commands with proper ``conf t`` and ``wr mem``
        commands for IOS-like devices.
        """
        @wraps(generate)
        def wrapped(*args, **kwargs):
            cmds = ['configure terminal']

            # Emit commands, append exit
            result = generate(*args, **kwargs)
            cmds.extend(result)
            status = ['changing password']
            cmds.append('exit')

            # Get the device object and use it to add the write mem
            try:
                #dev = args[1] # (self, device, ...)
                dev = args[0] # (device, commands, extra)
            except IndexError:
                dev = kwargs.get('device')
            cmds.extend(dev.commit_commands)
            status.extend(['saving config', 'done'])

            # Final list of commands
            #return cmds
            self.commands = cmds
            #print 'Sending %r to %s' % (cmds, dev)
            return self.commands

        return wrapped

    def to_a10(self, device, commands=None, extra=None):
        cmd = 'admin admin password %s'
        return [cmd]

    ARISTA_ADMIN_USER = 'admin'
    def to_arista(self, device, commands=None, extra=None):
        cmd = 'aaa {admin} secret 0 %s'.format(admin=ARISTA_ADMIN_USER)
        return [cmd]
    
    def to_aruba(self, device, commands=None, extra=None):
        cmd = 'mgmt-user admin %s' % self.new_password
        cmds = ['configure terminal', cmd, 'exit', 'commit apply']
        return cmds

    def to_brocade(self, device, commands=None, extra=None):
        # Brute force that this is a VDX switch
        if device.is_switch() and 'vdx' in device.make.lower():
            cmd = 'username admin password %s'
        # All other Brocade platforms
        else:
            cmd = 'enable super-user-password %s'

        return [cmd]

    def to_cisco(self, device, commands=None, extra=None):
        cmd = 'enable secret 0 %s'
        return [cmd]

    def to_citrix(self, device, commands=None, extra=None):
        cmd = 'set system user nsroot %s'
        return [cmd] + device.commit_commands

    def to_foundry(self, device, commands=None, extra=None):
        cmd = 'enable super-user-password %s'
        return [cmd]

    def to_juniper(self, device, commands=None, extra=None):
        """
        Returns a list of Junoscript commands as ElementTree Element XML objects.

        When passed to execute_junoscript output will look like this::

        <rpc><lock-configuration/></rpc>
        <rpc>
            <load-configuration action="replace">
                <configuration>
                    <system>
                        <root-authentication>
                            <encrypted-password>{MD5-CRYPT HASH}</encrypted-password>
                        </root-authentication>
                    </system>
                </configuration>
            </load-configuration>
        </rpc>
        <rpc><commit-configuration/></rpc>
        """
        #newpass = self.work[device]

        # Create lock-configuration element
        xml = [ET.Element('lock-configuration')]
        status = ['locking configuration']

        # Recursively add subelements to 'load-configuration' element. When
        # finished, set text to inner-most element ('encrypted-password') to the
        # value of self.new_password.
        load = ET.Element('load-configuration', action='replace')
        body = ET.SubElement(load, 'configuration')
        syst = ET.SubElement(body, 'system')
        root = ET.SubElement(syst, 'root-authentication')
        ET.SubElement(root, 'encrypted-password').text = crypt_md5(self.new_password)
        status.extend(['changing password', 'done'])

        # Tack on config/commit to output
        xml.append(load)
        xml.append(ET.Element('commit-configuration'))
        status.extend(['committing', 'done'])

        #print 'Sending %r to %s' % (xml, device)
        return xml

    def to_netscreen(self,device, commands=None, extra=None):
        cmd = 'set admin password %s' % self.new_password
        return [cmd, 'save config']

    def to_paloalto(self, device, commands=None, extra=None):
        """
        On PAN devices the password change takes effect immediately and does not
        require a commit.
        """
        crypt_pw = crypt_md5(self.new_password)
        cmd = 'set mgt-config users admin phash %s' % crypt_pw

        cmds = ['configure', cmd]
        return cmds

    def generate(self, device, commands=None, extra=None):
        """
        Simple override of base generate to do special stuff for IOS-like
        devices by wrapping it in the ``ioslike()`` decorator. 
        
        This is strictly to reduce boilerplate in all of the custom methods for
        each IOS-like vendor.
        """
        gen = self._super.generate
        commands = commands or self.commands
        if device.is_ioslike():
            # Wrap in ioslike decorator
            gen = self.ioslike(gen)

        return self.insert_password(gen, device, commands, extra)

    def insert_password(self, gen, device, commands, extra):
        """
        Use string replacement to insert the new password into the command
        string for each device.
        """
        #newpass = self.work[device]
        #print 'Setting password to %r on %s' % (newpass, device)
        cmds = gen(device, commands, extra)

        # Iterate the commands and use string replacement on the one with '%s'
        # found in it. Brute force? You betcha!
        for idx, cmd in enumerate(cmds):
            if '%s' in cmd:
                cmds[idx] = cmd % self.new_password
                break
        return cmds

    def parse(self, results, device):
        """Overload what to do when things complete"""
        log.msg('SUCCESS: %s' % device)

if __name__ == '__main__':
    log.startLogging(open('/tmp/pw.log', 'w'), setStdout=False)
    #devices = ['firewall']
    devices = ['netscreen']
    new_password = 'abc123'
    pw = ChangePassword(devices=devices, new_password=new_password,
            verbose=True)
    pw.run()
