"""
Loader for Trigger NetDevices using HPT API.
"""

from trigger.netdevices.loader import BaseLoader
from trigger.exceptions import LoaderFailed
import urllib
import urlparse
try:
    import requests
except ImportError:
    REQUESTS_AVAILABLE = False
else:
    REQUESTS_AVAILABLE = True
    

# Fiel mappings from HPT to Trigger to transform
TRANSFORM_FIELDS = {
    'node_name': 'nodeName',
}

class HollowpointLoader(BaseLoader):
    """
    Wrapper for loading metadata via Hollowpoint.

    To use this define ``NETDEVICES_SOURCE`` in this format::

        http(s)://host:port/api/inventory/?format=json&limit={limit}
    """
    is_usable = REQUESTS_AVAILABLE

    def get_data(self, url):
        """
        Query NetDevice objects from the Hollowpoint API.
        """
        # Hard-code admin:admin Basic auth right now...
        r = requests.get(url, auth=('admin', 'admin'))
        data = []

        # If we're good, return the results
        if r.ok:
            data = r.json()['results']

        return self.transform_fields(data)

    def transform_fields(self, data):
        """Transform the fields if they are present"""
        for d in data:
            for old, new in TRANSFORM_FIELDS.items():
                old_value = d.pop(old, None)
                if old_value is not None:
                    d[new] = old_value
        return data

    def load_data_source(self, data_source, **kwargs):
        """
        In this case path would be something like '/api/inventory' and kwargs is
        everything else.
        """
        path = data_source
        scheme = kwargs.get('scheme', 'https')
        host = kwargs.get('hostname')
        port = str(kwargs.get('port', ''))
        limit = kwargs.get('limit', 9999)
        format = kwargs.get('format', 'json')

        # Include the port in the host
        if port.isdigit():
            netloc = '%s:%s' % (host, port)
        else:
            netloc = host

        # Construct the query string
        params = '' # for now... we don't want params
        query = urllib.urlencode(dict(limit=limit, format=format))
        fragment = '' # for now... we don't want fragment

        # We're using this stuff to pass to urlparse.urlunparse
        url_tuple = (scheme, netloc, path, params, query, fragment)
        url = urlparse.urlunparse(url_tuple)

        try:
            return self.get_data(url)
        except Exception as err:
            raise LoaderFailed("Tried %r; and failed: %r" % (data_source, err))
