from django.shortcuts import render
from .forms import BookForm
from .drones import get_drones_of_user, get_all_drone_data


# Create your views here.
def dashboard(request):
    drones_data = get_drones_of_user(request.session['username'])
    context = {
        "username": request.session['username'],
        "drones_data": drones_data,
    }
    return render(request, '../../drone_system/templates/drone_system/dashboard.html', context)


def book(request):
    form = BookForm(request.POST or None)
    context = {
        "form": form
    }
    return render(request, '../../drone_system/templates/drone_system/book.html', context)


def information(request):
    drones_data = get_all_drone_data()
    context = {
        "drones_data": drones_data
    }
    return render(request, '../../drone_system/templates/drone_system/information.html', context)


def help(request):
    return render(request, '../../drone_system/templates/drone_system/help.html')
