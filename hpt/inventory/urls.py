from django.conf.urls import patterns, include, url
from rest_framework import routers
from inventory import views
router = routers.DefaultRouter()
router.register(r'inventory', views.NetDeviceViewSet)

urlpatterns = patterns(__name__,
    url(r'^', include(router.urls)),
)
