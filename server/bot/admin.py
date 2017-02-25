from django.contrib import admin
from django.contrib.auth.models import User, Group

from .models import *




admin.site.register(SwarmBot)

admin.site.register(DS)
admin.site.register(IR)
