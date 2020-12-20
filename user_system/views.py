from django.shortcuts import render
from django.shortcuts import redirect


# Create your views here.
def home_screen(request):
    return render(request, 'user_system/home.html')


def login(request):
    return render(request, 'user_system/login.html')


def information(request):
    return render(request, 'user_system/information.html')


def register(request):
    return render(request, 'user_system/register.html')


def wrong_home_address(request):
    return redirect('/home/')
