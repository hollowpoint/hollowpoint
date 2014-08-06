import json

def _prototype_netdevices(netdevices_file):
    """
    Load NetDevices data from prototype file to use it as columns.gq$

    :param netdevices_file:
        A NetDevices.json file
    """
    with open(netdevices_file, 'r') as f:
        data = json.load(f)
    return data[0].keys()
