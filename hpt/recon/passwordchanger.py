#!/usr/bin/env python -W ignore::DeprecationWarning
# -*- coding: utf-8 -*-

# passwordchanger.py - Password Changer using Commando library

import collections
from functools import wraps
from trigger.cmds import Commando
from trigger.netdevices import NetDevices
from trigger.utils import crypt_md5
import xml.etree.cElementTree as ET

import logging
log = logging.getLogger(__name__)

# Namedtuple for use by command-emitting functions that return a 2-tuple of
# (cmds, status)
CommandsStatus = collections.namedtuple('CommandsStatus', 'cmds status')

class PasswordChanger(Commando):
    """
    Change passwords on network devices.

    ``work`` should be a dictionary of {'device_name': 'password', ...}
    """
    def __init__(self, work, *args, **kwargs):
        self.work = work
        self.failures = {}
        self.production_only = kwargs.get('production_only', True)
        self.nd = NetDevices(with_acls=False, production_only=self.production_only)
        self._super = super(PasswordChanger, self)
        devices = self.work.keys()
        self._super.__init__(devices=devices, *args, **kwargs)

    def errback(self, reason, dev):
        """Catch the error and store the result."""
        self.failures[dev] = reason
        log.info('FAILURE: %s' % dev)

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

    def to_arista(self, device, commands=None, extra=None):
        cmd = 'aaa root secret %s'
        return [cmd]

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
        newpass = self.work[device]

        # Create lock-configuration element
        xml = [ET.Element('lock-configuration')]
        status = ['locking configuration']

        # Recursively add subelements to 'load-configuration' element. When
        # finished, set text to inner-most element ('encrypted-password') to the
        # value of newpass.
        load = ET.Element('load-configuration', action='replace')
        body = ET.SubElement(load, 'configuration')
        syst = ET.SubElement(body, 'system')
        root = ET.SubElement(syst, 'root-authentication')
        ET.SubElement(root, 'encrypted-password').text = crypt_md5(newpass)
        status.extend(['changing password', 'done'])

        # Tack on config/commit to output
        xml.append(load)
        xml.append(ET.Element('commit-configuration'))
        status.extend(['committing', 'done'])

        #print 'Sending %r to %s' % (xml, device)
        return xml

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
        newpass = self.work[device]
        #print 'Setting password to %r on %s' % (newpass, device)
        cmds = gen(device, commands, extra)

        # Iterate the commands and use string replacement on the one with '%s'
        # found in it. Brute force? You betcha!
        for idx, cmd in enumerate(cmds):
            if '%s' in cmd:
                cmds[idx] = cmd % newpass
                break
        return cmds

    def parse(self, results, device):
        """Overload what to do when things complete"""
        log.info('SUCCESS: %s' % device)

    # NYI because we haven't figured out how to bake in incrementals into the
    # Commando subclasses just yet. Not that it's impossible, just time
    # consuiming.
    """
    def update_board(results, dev=None):
        try:
            self.active[dev] = status[len(results)]
        except IndexError:
            pass

    def move_on(res, dev=None):
        if not dev:
            return None
        del self.active[dev]

    def complete(results, dev=None, extra=None):
        log.msg('SUCCESS: %s' % dev)

    def run_and_draw(self, stdscr, work, jobs, failures):
        active = {}
        start_qlen = len(work)
        start_time = time.time()

        if not stdscr:
            def redraw():
                pass

        else:
            def redraw():
                draw_screen(stdscr, work, active, failures, start_qlen,
                            start_time)

    def run(self):
        self.run_and_draw()
        self._super.run()
    """


def min_sec(secs):
    secs = int(secs)
    return '%d:%02d' % (secs / 60, secs % 60)

# NYI
"""
import curses
def draw_screen(s, work, active, failures, start_qlen, start_time):
    '''
    Curses-based status board.
    '''
    s.erase()

    # DO NOT cache the result of s.getmaxyx(), or you cause race conditions
    # which can create exceptions when the window is resized.
    def maxx():
        y, x = s.getmaxyx()
        return x
    def maxy():
        y, x = s.getmaxyx()
        return y

    s.addstr(0, 0, 'camaro_pc'[:maxx()], curses.A_BOLD)
    progress = '  %d/%d devices' % (start_qlen - len(work) - len(active),
                                    start_qlen)
    s.addstr(0, maxx() - len(progress), progress)

    doneness = 1 - float(len(work) + len(active)) / start_qlen
    elapsed = raw_time() - start_time
    elapsed_str = min_sec(elapsed)
    if doneness == 0:
        remaining_str = ' '
    elif doneness == 1:
        remaining_str = 'done'
    else:
        remaining_str = min_sec(elapsed / doneness - elapsed)
    max_line = int(maxx() - len(remaining_str) - len(elapsed_str) - 2)

    s.addstr(1, 0, elapsed_str)
    s.addstr(1, maxx() - len(remaining_str), remaining_str)
    s.hline(1, len(elapsed_str) + 1, curses.ACS_HLINE, int(max_line * doneness))

    if failures:
        count, plural = len(failures), (len(failures) > 1 and 's' or '')
        s.addstr(2, 0, ' %d failure%s, will report at end ' % (count, plural),
                 curses.A_STANDOUT)

    for y, (dev, status) in zip(range(3, maxy()), active.items()):
        s.addstr(y, 0, ('%s: %s' % (dev, status))[:maxx()], curses.A_BOLD)

    s.move(maxy() - 1, maxx() - 1)
    s.refresh()
"""