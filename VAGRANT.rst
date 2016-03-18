####################
Vagrant Instructions
####################

Don't pretend this is easy. This is why we write shit down.

Start it up::

    vagrant up

If for some reason it complains about VMWare because you happen to have them
both installed run this instead::

    vagrant up --provider virtualbox

Follow the Ubuntu 14.04 install instructions:

    https://docs.docker.com/engine/installation/linux/ubuntulinux/#install


Get Docker running and shit (Hint: ``docker run hello-world``)

Install
=======

See the Docker install instructions in README.rst.

If anything deviates from that, it will be here. Vague. I know.


Data directory
--------------

You might not have a ``/data`` tree. If no, do this::

    sudo mkdir -p /data/docker/registry
    sudo chgrp -R docker /data/docker
    sudo chmod g+w -R /data/docker

And now ``/data/docker`` is yours without sudo. You're welcome! Shut up.
