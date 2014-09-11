from django.conf.urls import patterns, include, url
from rest_framework import routers
from core import views

router = routers.DefaultRouter()
router.register(r'task', views.TaskStateViewSet)

urlpatterns = patterns(__name__,
    url(r'^', include(router.urls)),
)
