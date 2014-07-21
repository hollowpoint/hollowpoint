
import xmlrpclib

class SafeTransportWithCert(xmlrpclib.SafeTransport):
    __cert_file = '../ssl/client/client.crt'
    __key_file = '../ssl/client/client.key'

    def make_connection(self, host):
        host_with_cert = (host, {
            'key_file': self.__key_file,
            'cert_file': self.__cert_file
            })
        return xmlrpclib.SafeTransport.make_connection(self, host_with_cert)

transport = SafeTransportWithCert()
client = xmlrpclib.Server('https://trigger-server:9000', transport=transport)

# Or use python-requests to do SSL certificate authentication and validation:
# http://docs.python-requests.org/en/latest/user/advanced/#ssl-cert-verification

"""
# From Client host
import requests
url = 'https://trigger-server:9000'
r = requests.post(
    url,
    cert=('ssl/client/client.crt',
          'ssl/client/client.key'),
    verify='certs/rootCA.pem'
)
print r.content
"""
