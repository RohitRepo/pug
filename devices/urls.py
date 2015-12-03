from django.conf.urls import patterns, url, include

from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = patterns('',
                      url(r'^$', 'devices.views.add_device'),
                      url(r'^/my$', 'devices.views.user_devices'),
                      url(r'^/(?P<device_id>[0-9]+)/turn_on$', 'devices.views.device_on'),
                      url(r'^/(?P<device_id>[0-9]+)/turn_off$', 'devices.views.device_off'),
                    )

urlpatterns = format_suffix_patterns(urlpatterns)
