from django.conf.urls import patterns, include, url
from rest_framework import routers
from core import views


router = routers.DefaultRouter()
router.register(r'task', views.TaskStateViewSet)
router.register(r'task_meta', views.TaskMetaViewSet)


urlpatterns = patterns(__name__,
    url(r'^', include(router.urls)),
)
