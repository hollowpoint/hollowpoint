from django.shortcuts import render

# Create your views here.
from models import AccessList
from rest_framework import viewsets
from serializers import AccessListSerializer

class AccessListViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows AccessList objects to be viewed or edited.
    """
    queryset = AccessList.objects.all()
    serializer_class = AccessListSerializer
