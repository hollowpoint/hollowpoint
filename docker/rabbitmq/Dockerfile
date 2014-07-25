# Build RabbitMQ with admin:admin user and mgmt, federation, and SSL auth plugins enabled
FROM ubuntu:14.04
MAINTAINER Jathan McCollum <jathan@gmail.com>

# Reduce output from debconf
ENV DEBIAN_FRONTEND noninteractive
ENV PATH /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

# Initialize apt-get
#RUN apt-get update -qqy
RUN apt-get update -y
RUN apt-get install -y wget

# Add the RabbitMQ repo
RUN echo "deb http://www.rabbitmq.com/debian/ testing main" >> /etc/apt/sources.list.d/rabbitmq.list
RUN wget --quiet -O - http://www.rabbitmq.com/rabbitmq-signing-key-public.asc | apt-key add -
RUN apt-get update -y

# Docker work around for upstart: [https://github.com/dotcloud/docker/issues/1024]
#RUN dpkg-divert --local --rename --add /sbin/initctl
#RUN ln -s /bin/true /sbin/initctl

# Install RabbitMQ and enable the plugins
RUN apt-get install -y rabbitmq-server
RUN rabbitmq-plugins enable rabbitmq_management
RUN rabbitmq-plugins enable rabbitmq_federation
RUN rabbitmq-plugins enable rabbitmq_federation_management
RUN rabbitmq-plugins enable rabbitmq_auth_mechanism_ssl

# Configure it with an admin user (for now) instead of enabling guest:guest
#RUN rabbitmqctl add_user admin admin
#RUN rabbitmqctl set_user_tags admin administrator
#RUN rabbitmqctl set_permissions -p / admin '.*' '.*' '.*'
RUN echo "[{rabbit, [{loopback_users, []}]}]." > /etc/rabbitmq/rabbitmq.config

# For RabbitMQ and RabbitMQ Admin
EXPOSE 5672 15672

ENTRYPOINT ["/usr/sbin/rabbitmq-server"]
