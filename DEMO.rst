###############
Demo QuickStart
###############

This is the quick start for the demo as of 2016-03-11. The latest latest!

This assumes an Vagrant VM that already has Docker and the RabbitMQ, Postgres,
and Redis images installed on it.

Server
======

Get the server running::

    $ vagrant up

Login and start the services::

    $ vagrant ssh
    $ docker start postgres
    $ docker start rabbitmq
    $ docker start redis

This server will be available to the other services at ``192.168.33.10``.

Localhost
=========

Start Device VMs
----------------

Make sure Virtualbox is running and you've started VMs for:

+ vEOS (``arista-sw1`` )
+ juniper_srx (``juniper-fw``)

Setup
-----

On localhost, open up five (5) terminals. Yes, five.

In each terminal run this::

    $ cd ~/src/hollowpoint
    $ export TRIGGER_HOST=localhost
    $ export TRIGGER_PORT=9000

Services
--------

After setup, do this for each distinct terminal...

Terminal 1: Trigger XMLRPC::

    $ cd xmlrpc
    $ ./start_xmlrpc.sh

Terminal 2: Flower::

    $ ./start_flower.sh

... Next, you'll setup Django and create the database tables for the app.

Terminal 3: Django::

    $ python hpt/manage.py syncdb  # When prompted create a superuser
    $ python hpt/manage.py migrate
    $ ./start_web.sh

Terminal 4: Celerycam::

    $ ./start_celerycam.sh

Terminal 5: Worker::

    $ ./start_worker.sh

Ports
-----

RabbitMQ
    http://guest:guest@192.168.33.10:15672

Web
    http://localhost:8100

Flower
    http://localhost:5555

Add Devices
-----------

Last step is add database entries for the 2 devices.

+ Go to web UI at http://localhost:8100
+ Create devices entries for 2 devices.

Python Shell
============

Last, open a 6th terminal and perform the setup steps above. Then::

    $ python hpt/manage.py shell_plus
    >>> from core import tasks
    >>> from celery import registry
    >>> show_clock = registry.tasks['core.tasks.show_clock']

To run ``show_clock()`` on devices::

    >>> devices = ['arista-sw1']
    >>> result = show_clock.delay(devices=devices)

+ Inspect results.
+ Illustrate how:

  - Worker picks it up
  - Celerycam snapshots it
  - Trigger XMLRPC service connects and does stuff and returns a result
  - Results reflected in Web UI, Python shell, in Flower

+ Talk about how NSoT could easily replace this inventory system, or plug into
  it with a little work. 
