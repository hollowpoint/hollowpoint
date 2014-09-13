from models import AccessList
from rest_framework import serializers

class AccessListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AccessList
