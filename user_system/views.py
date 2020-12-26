from django.shortcuts import render
from django.shortcuts import redirect
from .forms import RegisterForm, LoginForm
from .models import users


# Create your views here.
def home_screen(request):
    return render(request, 'user_system/home.html')


def information(request):
    return render(request, 'user_system/information.html')


def login(request):
    # try:
    #     if request.session['username']:
    #         return redirect('/dashboard/')
    # except KeyError:
    #     form = LoginForm(request.POST or None)
    #     login_status = None
    #     if form.is_valid():
    #         if users.objects.filter(username=form.cleaned_data['username'], password=form.cleaned_data['password']):
    #             request.session['username'] = form.cleaned_data['username']
    #             return redirect('/dashboard/')
    #         else:
    #             login_status = "wrong_credentials"
    #     form = LoginForm()
    #     context = {
    #         "form": form,
    #         "login_status": login_status,
    #     }
    #     return render(request, 'user_system/login.html', context)
    if 'username' not in request.session:
        form = LoginForm(request.POST or None)
        login_status = None
        if form.is_valid():
            if users.objects.filter(username=form.cleaned_data['username'], password=form.cleaned_data['password']):
                request.session['username'] = form.cleaned_data['username']
                return redirect('/dashboard/')
            else:
                login_status = "wrong_credentials"
        form = LoginForm()
        context = {
            "form": form,
            "login_status": login_status,
        }
        return render(request, 'user_system/login.html', context)
    else:
        return redirect('/dashboard/')


def register(request):
    form = RegisterForm(request.POST or None)
    registration = None
    if form.is_valid():
        if not users.objects.filter(username=form.cleaned_data['username']):
            form.save()
            registration = "successful"
        else:
            registration = "exists"
        form = RegisterForm()
    context = {
        "form": form,
        "registration_status": registration
    }
    return render(request, 'user_system/register.html', context)


def wrong_home_address(request):
    return redirect('/home/')
