from django.conf.urls import url
from django.contrib import admin

from .views import *

urlpatterns = [


###webpages
    url(r'^$', index, name = 'index'),
    url(r'^sensors/$', sensorView, name='sensorView'),


###Raspi's data to the server

    url(r'^matrixUpdate/(?P<swarmBotId>\d+)/(?P<block>\d+)/$', matrixUpdate, name='matrixUpdate'),
    url(r'^patchStatusUpdate/(?P<swarmBotId>\d+)/$', patchStatusUpdate, name='patchStatusUpdate'),
    url(r'^sensor_readings/$', sensorReadView), #coming from raspis


###Ajax in sensor.html

    url(r'^ds_reading/(?P<id>\d+)/$', dsvalue, name = 'ds'),
    url(r'^ir_reading/(?P<id>\d+)/$', irvalue, name = 'ldr'),
    url(r'^patchStatus/(?P<id>\d+)/$', patchStatus, name = 'patchStatus'),
    url(r'^blockCheck/(?P<id>\d+)/$', blockCheck, name = 'mat'),

]
