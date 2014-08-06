from django.conf.urls import patterns, include, url

import xadmin
xadmin.autodiscover()

#from xadmin.plugins import xversion
#xversion.register_models()

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'hpt.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # Admin
    url(r'^admin/', include(admin.site.urls)),

    # Xadmin
    url(r'^', include(xadmin.site.urls)),

    # Change password
    url(r'^change_password/', 'api.views.change_password'),
)

from django.conf import settings
if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
