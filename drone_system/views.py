from django.shortcuts import render


# Create your views here.
def dashboard(request):
    context = {
        "username": request.session['username']
    }
    return render(request, '../../drone_system/templates/drone_system/dashboard.html', context)


def book(request):
    return render(request, '../../drone_system/templates/drone_system/book.html')


def information(request):
    return render(request, '../../drone_system/templates/drone_system/information.html')


def help(request):
    return render(request, '../../drone_system/templates/drone_system/help.html')
