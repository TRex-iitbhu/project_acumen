from django.conf.urls import url
from django.contrib import admin

from .views import *

urlpatterns = [


###webpages
    url(r'^$', index, name = 'index'),
    url(r'^sensors/$', sensorView, name='sensorView'),


###Raspi's data to the server

    url(r'^matrixUpdate/(?P<swarmBotId>\d+)/(?P<row>\d+)/(?P<col>\d+)/$', matrixUpdate, name='matrixUpdate'),
    url(r'^sensor_readings/$', sensorReadView), #coming from raspis


###Ajax in sensor.html

    url(r'^ds_reading/(?P<id>\d+)/$', dsvalue, name = 'ds'),
    url(r'^ldr_reading/(?P<id>\d+)/$', ldrvalue, name = 'ldr'),
    url(r'^patchStatus/(?P<id>\d+)/$', patchStatus, name = 'patchStatus'),
    url(r'^matUpdateWeb/(?P<id>\d+)/$', matUpdateWeb, name = 'mat'),

]
