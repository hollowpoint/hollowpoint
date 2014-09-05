from models import NetDevice
from rest_framework import serializers

class NetDeviceSerializer(serializers.HyperlinkedModelSerializer):
    nodeName = serializers.CharField(max_length=255)

    class Meta:
        model = NetDevice
        fields = ('nodeName', 'manufacturer', 'deviceType', 'make', 'model',
                  'adminStatus')
