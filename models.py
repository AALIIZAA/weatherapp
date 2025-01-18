from django.db import models
from django.contrib.auth.models import User


class Register(models.Model):
    username=models.CharField(max_length=50,default="none")
    email=models.CharField(max_length=30,default="none")
    password=models.CharField(max_length=20)
    role = models.CharField(max_length=50, choices=[('admin', 'Admin'), ('pro_user', 'Pro User'), ('normal_user', 'Normal User')])
    def __str__(self):
        return self.username+" "+self.email
    



class SensorData(models.Model):
    temperature = models.FloatField()
    pressure = models.FloatField()
    altitude = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=[('current', 'Current'), ('past', 'Past')], default='current')

    def __str__(self):
        return f"Temperature: {self.temperature}°C, Pressure: {self.pressure} hPa, Altitude: {self.altitude} m"
