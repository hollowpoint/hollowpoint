from models import NetDevice
from rest_framework import serializers

class NetDeviceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = NetDevice
        fields = ('node_name', 'manufacturer', 'deviceType', 'make', 'model',
                  'adminStatus', 'acls')
