from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^fuzzyapp/', include('fuzzyapp.urls', namespace="fuzzyapp")),
    url(r'^admin/'   , include(admin.site.urls)),
)
