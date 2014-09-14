from django.shortcuts import render

# Create your views here.
from models import NetDevice
from rest_framework import viewsets
from serializers import NetDeviceSerializer

class NetDeviceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows NetDevice objects to be viewed or edited.
    """
    queryset = NetDevice.objects.all()
    serializer_class = NetDeviceSerializer
    #model = NetDevice

from django.views.generic import TemplateView, ListView, DetailView
'''
class NetDeviceView(TemplateView):
    model = NetDevice
    template_name = 'inventory/list.html'
netdevice_view = NetDeviceView.as_view()
'''
class NetDeviceList(ListView):
    model = NetDevice

netdevice_list = NetDeviceList.as_view()
