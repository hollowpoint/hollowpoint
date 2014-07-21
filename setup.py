#!/usr/bin/env python


try:
    from setuptools import setup, find_packages, Command
except ImportError:
    raise SystemExit('We require setuptools. Sorry! Install it and try again: http://pypi.python.org/pypi/setuptools')
import os
import sys

# Get version from pkg index
from hollowpoint import __version__

# Names of required packages
requires = [
]

class CleanCommand(Command):
    user_options = []
    def initialize_options(self):
        self.cwd = None
    def finalize_options(self):
        self.cwd = os.getcwd()
    def run(self):
        os.system ('rm -rf ./build ./dist ./*.pyc ./*.tgz ./*.egg-info')


desc = 'Hollowpoint'
long_desc = '''
This is a stub for the Hollowpoint project.

Hollowpoint is a modular and extensible network infrastructure control platform.
'''

setup(
    name='hollowpoint',
    version=__version__,
    author='Jathan McCollum',
    author_email='jathan@hollowpt.com',
    packages=find_packages(exclude=['tests']),
    license='Apache License 2.0',
    #url='https://github.com/foo/bar',
    description=desc,
    long_description=long_desc,
    scripts=[],
    include_package_data=True,
    install_requires=requires,
    keywords = [
        'Configuration Management',
        'IANA',
        'IEEE',
        'IP',
        'IP Address',
        'IPv4',
        'IPv6',
        'Firewall',
        'Network Automation',
        'Networking',
        'Network Engineering',
        'Network Configuration',
        'Systems Administration',
        'Switch',
    ],
    classifiers = [
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Environment :: Console :: Curses',
        'Environment :: Web Environment',
        'Framework :: Twisted',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Other Audience',
        'Intended Audience :: Science/Research',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Telecommunications Industry',
        'Natural Language :: English',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet',
        'Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator',
        'Topic :: Security',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Networking',
        'Topic :: System :: Networking :: Monitoring',
        'Topic :: System :: Operating System',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities',
    ],
    cmdclass={
        'clean': CleanCommand
    }
)
