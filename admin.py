from django.contrib import admin
from weatherproject.models import Register
from weatherproject.models import SensorData

admin.site.register(Register)

admin.site.register(SensorData)
