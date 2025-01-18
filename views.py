from django.shortcuts import render, HttpResponse,redirect
from django.contrib.auth import authenticate,login
from weatherproject.models import Register
from .models import SensorData
import requests
from requests.exceptions import RequestException
import serial
import time
from django.core.paginator import Paginator

def register(request):
    if request.method == 'POST':
        uname = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        role = request.POST['role']

        if password != password2:
            return render(request, "register.html", {"error": "Passwords do not match."})

        print(uname, email, password, password2, role)
        
        user = Register(username=uname, email=email, password=password, role=role)
        user.save()
        print("The data has been written in db")

    return render(request, "register.html")

        

def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        role = request.POST['role']

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            
            if role == 'super_user' and user.is_superuser:
                return redirect('dashboard')  
            elif role == 'normal_user' and not user.is_superuser:
                return redirect('normaluser') 
            
            else:
                return render(request, 'login.html', {'error': 'Invalid role for this user'})
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    
    return render(request, "login.html")


def dashboard(request):
    try:
        ser = serial.Serial("COM4", 115200)  
        data = ser.readline().decode().strip()
        ser.close()  
    except serial.SerialException as e:
        data = f"Error: {e}"


    if request.user.profile.is_pro:
        return render(request, 'prouser.html', {'data': data})  
    else:
        return render(request, 'normaluser.html', {'data': data}) 

def normaluser(request):
    return render(request,'normaluser.html')

def superuser(request):
    return render(request,'superuser.html')

def sensor_dashboard(request):
    
    latest_data = SensorData.objects.all().order_by('-timestamp')[:10]  
    return render(request, 'sensor_dashboard.html', {'latest_data': latest_data})


def receive_data(request):
    if request.method == 'GET':
        temperature = request.GET.get('temperature')
        pressure = request.GET.get('pressure')
        altitude = request.GET.get('altitude')

        if temperature and pressure and altitude:
            past_data = SensorData.objects.filter(status='current')
            past_data.update(status='past')

            sensor_data = SensorData(
                temperature=temperature,
                pressure=pressure,
                altitude=altitude,
                status='current'
            )
            sensor_data.save()

            print(f"New sensor data saved as current: {sensor_data}")

            return HttpResponse('Data received and saved successfully')
        else:
            return HttpResponse('Missing data', status=400)
    else:
        return HttpResponse('Invalid request method', status=405)

def index(request):
    if request.user.is_superuser:
        data = SensorData.objects.all()
    else:
        data = SensorData.objects.filter(timestamp__gte=now()-timedelta(days=1))
    
    paginator = Paginator(data, 25)  # Show 25 records per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'index.html', {'page_obj': page_obj})
