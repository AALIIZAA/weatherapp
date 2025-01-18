from django.urls import path , include
from django.contrib import admin
from . import views
from django.contrib.auth import views as auth_views

admin.site.site_title="Welcome to Weather Station"
admin.site.site_header="Weather Station"
admin.site.site_index_title='Database'

urlpatterns = [
    path('register', views.register, name='register'),
    path('', views.custom_login, name='custom_login'),  
    path('dashboard', views.dashboard, name='dashboard'), 
    path('normaluser',views.normaluser,name='normaluser'),
    path('superuser',views.superuser,name='superuser'),  
    path('sensor_dashboard',views.sensor_dashboard,name='sensordashboard'),
    path('receive_data/', views.receive_data, name='receive_data'),
    path('index', views.index,name='index'),
]


