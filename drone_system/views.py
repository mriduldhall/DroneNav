from django.shortcuts import render
from .drones import get_drones_of_user


# Create your views here.
def dashboard(request):
    drones_data = get_drones_of_user(request.session['username'])
    context = {
        "username": request.session['username'],
        "drones_data": drones_data,
    }
    return render(request, '../../drone_system/templates/drone_system/dashboard.html', context)


def book(request):
    return render(request, '../../drone_system/templates/drone_system/book.html')


def information(request):
    return render(request, '../../drone_system/templates/drone_system/information.html')


def help(request):
    return render(request, '../../drone_system/templates/drone_system/help.html')
