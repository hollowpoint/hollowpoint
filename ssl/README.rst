################
SSL Certificates
################

Cutting certs
=============

Cutting a new CA (ends up in ``ca/cacert.pem``)::

    ./setup_ca.sh [Common Name (CN)]

Cutting a new server cert (ends up in ``server/[hostname]*`` including cert, key, p12)::

    ./make_server_cert.sh [hostname] [password]

Cutting a new client cert::

    ./create_client_cert.sh [client name] [password]

*NOTE:* Password for all certs created so far is 'rabbit'.

Configuring RMQ for SSL
=======================

Put this in ``/etc/rabbitmq/rabbitmq.config`` (e.g. if your hostname is
*server*)::

    % RabbitMQ config is Erlang. Erlang comments begin with "%"
    [
        {rabbit, [
            % Allow "guest" to login from WebUI
            {loopback_users, []},
            % Listen on default port non-SSL
            {tcp_listeners, [5672]},
            % Enable SSL
            {ssl_listeners, [5673]},
            {ssl_options, [
                {cacertfile, "/etc/rabbitmq/ssl/ca/cacert.pem"},
                {certfile, "/etc/rabbitmq/ssl/server/server.cert.pem"},
                {keyfile, "/etc/rabbitmq/ssl/server/server.key.pem"},
                {verify, verify_peer},
                {fail_if_no_peer_cert, true}
            ]}
        ]}
    ].
