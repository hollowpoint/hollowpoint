To start a new unit, we need to tell systemd to create the symlink and then
start the file::

    $ sudo systemctl enable /etc/systemd/system/rabbitmq.service
    $ sudo systemctl start rabbitmq.service

And then you can read the unit's output with ``journalctl``::

    $ journalctl -f -u rabbitmq.service

Do this for each service, making sure you put them into ``/etc/systemd/system``.
