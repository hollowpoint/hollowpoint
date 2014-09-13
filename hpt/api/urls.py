from django.conf.urls import patterns, include, url
from rest_framework import routers

import acls.views
import inventory.views

router = routers.DefaultRouter()
router.register(r'acls', acls.views.AccessListViewSet)
router.register(r'inventory', inventory.views.NetDeviceViewSet)

urlpatterns = patterns(__name__,
    url(r'^', include(router.urls)),
)
