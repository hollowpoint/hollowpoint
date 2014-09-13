from django.conf.urls import patterns, include, url
from rest_framework import routers
from acls import views
router = routers.DefaultRouter()
router.register(r'acls', views.AccessListViewSet)

urlpatterns = patterns(__name__,
    url(r'^', include(router.urls)),
)
