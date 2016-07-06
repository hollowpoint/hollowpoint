from django.conf.urls import patterns, include, url

# import xadmin
# xadmin.autodiscover()

#from xadmin.plugins import xversion
#xversion.register_models()

from django.contrib import admin
admin.autodiscover()

"""
from rest_framework import routers
from inventory import views
router = routers.DefaultRouter()
router.register(r'inventory', views.NetDeviceViewSet)
"""

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'hpt.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # Admin
    url(r'^admin/', include(admin.site.urls)),

    # Xadmin
    # url(r'^', include(xadmin.site.urls)),
    url(r'^', include(admin.site.urls)),

    # Change password
    url(r'^change_password/', 'core.views.change_password'),

    # Inventory API
    #url(r'^api/', include(router.urls)),
    #url(r'^api/', include('inventory.urls')),
    #url(r'^api/', include('core.urls')),
    url(r'^api/', include('api.urls')),

    # Django REST Framework
    url(r'^api-auth/', include('rest_framework.urls',
        namespace='rest_framework')),

    # Inventory
    url(r'^netdevices/$', 'inventory.views.netdevice_list'),
)

#from django.conf import settings
#if settings.DEBUG:
#    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
#    urlpatterns += staticfiles_urlpatterns()
