#!/usr/bin/env python

import sys
from twisted.python import log
log.startLogging(sys.stdout, setStdout=False)

from twisted.internet import ssl, reactor
from twisted.internet.protocol import Factory, Protocol
from trigger.contrib.xmlrpc.server import TriggerXMLRPCServer

# Extra
from twisted.application.service import Application
from twisted.web import xmlrpc, server


if __name__ == '__main__':

    rpc = TriggerXMLRPCServer()
    xmlrpc.addIntrospection(rpc)

    server_factory = server.Site(rpc)

    with open('../ssl/ca/rootCA.pem') as certAuthCertFile:
        certAuthCert = ssl.Certificate.loadPEM(certAuthCertFile.read())

    with open('../ssl/server/server.key') as keyFile:
        with open('../ssl/server/server.crt') as certFile:
            serverCert = ssl.PrivateCertificate.loadPEM(
                keyFile.read() + certFile.read())

    contextFactory = serverCert.options(certAuthCert)
    reactor.listenSSL(9000, server_factory, contextFactory)
    reactor.run()
