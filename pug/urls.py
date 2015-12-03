from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin

# WebClient urls
urlpatterns = patterns('',
                      url(r'^admin/', include(admin.site.urls)),
                      url(r'^$', 'accounts.clientViews.site_main', name='home'),
                      url(r'^home$', 'accounts.clientViews.user_profile', name="profile"),
               )


# API urls
urlpatterns += patterns('',
                       url(r'^api/v1/users', include('accounts.urls')),
                       url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
               )