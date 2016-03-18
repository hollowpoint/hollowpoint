from django.conf.urls import patterns, include, url
from rest_framework import routers

import acls.views
import inventory.views
import core.views


router = routers.DefaultRouter()
router.register(r'acls', acls.views.AccessListViewSet)
router.register(r'inventory', inventory.views.NetDeviceViewSet)
router.register(r'task', core.views.TaskStateViewSet)
router.register(r'task_meta', core.views.TaskMetaViewSet)
router.register(r'workers', core.views.WorkerStateViewSet)


urlpatterns = patterns(__name__,
    url(r'^', include(router.urls)),
)
