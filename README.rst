###########
Hollowpoint
###########

Infrastructure Control Platform

SSL and RabbitMQ
================

Enabling SSL support in RabbitMQ
    https://www.rabbitmq.com/ssl.html#enabling-ssl

Configuring SSL for RabbitMQ
    http://www.gettingcirrius.com/2013/01/configuring-ssl-for-rabbitmq.html

What's in this repo?
====================

certs
    Deprecated, use ssl

rabbitmq
    Rabbitmq configs/ettings

ssl
    Self-signed CA for Hollowpoint, client, and server certificates. Just copy this
    directory in its entirety to a server and reference the certs from there.

xmlrpc
   Trigger XMLRPC server stuff modified to perform certificate authentication.

RabbitMQ on RHEL 6.5
====================

Get the RPMs
------------

First you must, enable EPEL::

    sudo rpm -ivh http://mirrors.syringanetworks.net/fedora-epel/6/i386/epel-release-6-8.noarch.rpm

Erlang
~~~~~~

Use ``repotrack`` to download all of the erlang packages and it's dependent
packages from epel (`Source <http://unix.stackexchange.com/a/50671/982>`_)::

    mkdir erlang-packages
    repotrack -r epel -a x86_64 -p erlang-packages erlang

It downloads some i686 packages, and we don't want those, so ditch them::

    rm erlang-packages/*i686*.rpm

Now you have all of the erlang dependencies that aren't part of rhel6 core in
the ``erlang-packages`` directory.

RabbitMQ
~~~~~~~~

Download the latest RPM (version 3.3.1)::

    wget http://www.rabbitmq.com/releases/rabbitmq-server/v3.3.1/rabbitmq-server-3.3.1-1.noarch.rpm

Dependent libs
~~~~~~~~~~~~~~

Before you can install, you'll need to install the pre-requisites from rhel6.

Run ``yum provides`` on each of them to find out which packages need to be
installed first. You can pip the RPM install command to a file
(``dep-libs.txt``), like so::

    sudo rpm -ivh erlang-packages/*.rpm rabbit*.rpm 2> dep-libs.txt

Ok, now you can find out what packages you need to install. Ok, here goes a one-liner (trust me)::

    cat dep-libs.txt | awk '{print $1}' | cut -d '(' -f 1 | xargs yum provides | egrep -v '(^$|Repo|Matched|Other|Loaded)' | awk '{print $1}' | cut -d ':' -f 2 | sort | uniq > rhel6-packages.txt

And now you have all of those packages in ``rhel6-packages.txt``, and for
conciseness (we don't want the i686 packages) they are::

    libXxf86vm
    mesa-libGL
    mesa-libGLU
    SDL
    tk
    unixODBC

See below for installing.

Install the RPMs
----------------

First install the RHEL6 libs (note that we're disabling EPEL)::

    sudo yum --disablerepo=epel install libXxf86vm mesa-libGL mesa-libGLU SDL tk unixODBC

Now install the RPMS::

    sudo yum --disablerepo=epel install erlang-packages/*.rpm rabbit*.rpm

If everything installed without complaints, let's see if it works!

Init RabbitMQ
-------------

Configure it to launch on startup::

    sudo chkconfig --add rabbitmq-server
    sudo chkconfig --level 3 rabbitmq-server on

Ok let's get those plugins enabled::

    sudo rabbitmq-plugins enable rabbitmq_federation rabbitmq_federation_management rabbitmq_auth_mechanism_ssl

Start RabbitMQ
--------------

Does it work?!::

    sudo service rabbitmq-server start

And create the initial admin user (we can always delete him later)::

    sudo rabbitmqctl add_user admin admin
    sudo rabbitmqctl set_user_tags admin administrator
    sudo rabbitmqctl set_permissions -p / admin '.*' '.*' '.*'

Copy over the ssl directory (for certs)::

    sudo cp -a ssl /etc/rabbitmq
    sudo cp rabbitmq/rabbitmq.config.sample /etc/rabbitmq.config

And now replace the hostname in the certs (as root)::

    sed 's/\[HOSTNAME\]/'"${HOSTNAME}"'/' < rabbitmq/rabbitmq.config.sample > /etc/rabbitmq/rabbitmq.config

Or just edit it and replace ``[HOSTNAME]`` with the system hostname...

Now restart the server and we're gold::

    sudo service rabbitmq-server restart

PostgreSQL
==========

Enable the yum repo
-------------------

Instructions
    http://www.postgresql.org/download/linux/redhat/

::

    sudo yum install http://yum.postgresql.org/9.3/redhat/rhel-6-x86_64/pgdg-redhat93-9.3-1.noarch.rpm

Get the RPMs
------------

We'll be using ``repotrack`` again::

    mkdir pgsql-packages
    repotrack -r pgdg93 -a x86_64 -p pgsql-packages postgresql93-server

Install the RPMs
----------------

This time it's a lot simpler. They just work::

    sudo yum --disablerepo=pgdg93 install pgsql-packages/*.rpm

Init Postgres
-------------

Initialize the database services (this can take a while)::

    sudo service postgresql-9.3 initdb

Configure it to launch on startup::

    sudo chkconfig --add postgresql-9.3
    sudo chkconfig --level 3 postgresql-9.3 on

Configure Postgres
------------------

Put this at the bottom of ``pg_hba.conf``::

    # Stuff for Trigger/Hollowpoint
    host    all         all         10.20.30.0/24        trust
    host    all         all         10.20.30.0/24       trust

Change this inside of ``postgresql.conf``::

    # listen_addresses = 'localhost'
    listen_addresses = '*'

Configure replication
~~~~~~~~~~~~~~~~~~~~~

There is replication stuff we need to consider inside of ``pg_hba.conf``, but
isn't baked in that will need to be done at the cluster level that will look
something like this (don't implement this yet until we have it finalized)::

    host    replication replication 10.20.30.0/24       trust
    host    replication postgres    10.20.30.0/24       trust

Start it up!!
-------------

Does it work??::

    sudo service postgresql-9.3 start

Ok, good, now create the Hollowpoint database::

    sudo su - postgres
    createdb hpt

And now remove external repos
=============================

We're done installing, we may now disable the external repos::

    sudo yum remove epel-release pgdg-redhat93

Steps for a fresh system
========================

If you've already got the RPMs in a directory...

1. Don't install EPEL or PGDG repos, because we're not using them.
2. When you install packages using yum exclude ``--disablerepo=foo``
3. The rest of the instructions flow like butter. It took about 10 minutes
   from kickstart to manual config and install to get a new netbot box
   running.

Ubuntu
======

These instructions assume Ubuntu 12.04 and need to be updated.

System
------

::

    apt-get install -y git vim zsh screen

RabbitMQ
--------

Install
~~~~~~~

::

    echo "deb http://www.rabbitmq.com/debian/ testing main" >> /etc/apt/sources.list
    apt-get install -y wget
    wget http://www.rabbitmq.com/rabbitmq-signing-key-public.asc -O /tmp/rabbitmq-signing-key-public.asc
    apt-key add /tmp/rabbitmq-signing-key-public.asc
    apt-get -y update
    apt-get install -y rabbitmq-server

Configure
~~~~~~~~~

Enable plugins::

    rabbitmq-plugins enable rabbitmq_management
    rabbitmq-plugins enable rabbitmq_federation
    rabbitmq-plugins enable rabbitmq_federation_management
    #echo "[{rabbit, [{loopback_users, []}]}]." > /etc/rabbitmq/rabbitmq.config

Python
------

Install pip and virtualenv::

    apt-get install -y python-dev python-setuptools python-pip python-virtualenv
    sudo pip install virtualenvwrapper jedi

PostgreSQL
----------

Create ``/etc/apt/sources.list.d/pgdg.list``::

    echo "deb http://apt.postgresql.org/pub/repos/apt/ precise-pgdg main" >> /etc/apt/sources.list.d/pgdg.list

Import keys::

    wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -

Install
-------

::

    sudo apt-get update
    sudo apt-get upgrade
    sudo apt-get install -y postgresql-9.3 pgadmin3 libpq-dev

Trigger
-------

::

    mkvirtualenv hpt
    workon hpt
    pip install trigger

Starting Services
=================

First start Trigger's XMLRPRC service::

    twistd trigger-xmlrpc -p 9000 -s 9001

The remaining services include the Web UI, API, Flower monitor, and Celerycam
are managed using supervisord and the ``django-supervisor`` plugin. To start
services it's as simple as::

    python hpt/manage.py supervisor

All services will automatically start. You may inspect them like so::

    python hpt/manage.py supervisor status

Docker
======

RabbitMQ
--------

To have RabbitMQ listen on the proper ports (5672/tcp, 15672/tcp)::

    docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 jathanism/rabbitmq

Redis
-----

To have Redis listen on the proper ports (6379/tcp)::

    docker run -d --name redis -p 6379:6379 redis:2.8.12

PostgreSQL
----------

Start it up::

    docker run -d --name postgres -p 5432:5432 postgres:latest

Connect to the database using ``psql``::

    docker run -it --rm --link postgres:db postgres:latest sh -c 'exec psql -h "$DB_PORT_5432_TCP_ADDR" -p "$DB_PORT_5432_TCP_PORT" -U postgres'

Create the database from the ``postgres=#`` prompt::

    create database hpt;

If you're using ``DATABASE_URL``, set it like so::

    export DATABASE_URL=postgres://postgres@127.0.0.1:5432/hpt

Registry
--------

Running a custom registry that stores the stuff in ``/data/docker/registry``::

    docker run -d -p 5000:5000 -v /data/docker/registry:/tmp/registry --name registry registry:latest

Then you can tag an existing image with ``localhost:5000`` as the user::

    docker tag jathanism/rabbitmq localhost:5000/rabbitmq

And then push it to the registry::

    docker push localhost:5000/rabbitmq  # But why would I do this?
