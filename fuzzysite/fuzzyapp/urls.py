from django.conf.urls import patterns, url

from fuzzyapp import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<db_name>\w+)/$', views.db_information, name='db_information'),
)