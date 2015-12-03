from django.conf.urls import patterns, url, include

from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = patterns('',
                      url(r'^/login$', 'accounts.views.login_user'),
                      url(r'^/logout$', 'accounts.views.logout_user'),
                      url(r'^/currentUser$', 'accounts.views.get_current_user'),
                    )

urlpatterns = format_suffix_patterns(urlpatterns)
