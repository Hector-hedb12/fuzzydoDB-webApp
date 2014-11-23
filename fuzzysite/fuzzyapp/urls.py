from django.conf.urls import patterns, url

from fuzzyapp import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^db/(?P<db_name>\w+)/$', views.db_information, name='db_information'),
    url(r'^db/(?P<db_name>\w+)/info/$', views.db_info, name='db_info')
    
)
