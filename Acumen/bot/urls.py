from django.conf.urls import url
from django.contrib import admin

from .views import *

urlpatterns = [
    url(r'^$', LDRView, name = 'ldr'),

    url(r'^LDR/(?P<swarmBotId>\d+)/(?P<ldr_reading>\d+)/$', LdrPostView, name = 'ldr'),
    url(r'^DS/(?P<swarmBotId>\d+)/(?P<ds_reading>\d+)/$', DsPostView, name = 'ds'),
    url(r'^sensors/$', sensorView, name='sensorView'),
    url(r'^matrixUpdate/(?P<swarmBotId>\d+)/(?P<reading>\d+)/$', matrixUpdate, name='matrixUpdate'),
    url(r'^sensor_readings/$', sensorReadView),
    url(r'^ds_reading/(?P<id>\d+)/$', dsvalue, name = 'ds'),

]
