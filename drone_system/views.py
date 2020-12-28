from django.shortcuts import render
from django.shortcuts import redirect
from .forms import BookForm, ChangePassword, DeleteAccount, FutureBook
from .settings import validate_password, change_password, delete_account
from .drones import get_drones_of_user, get_all_drone_data, find_available_drone, assign_booking, find_earliest_drone, create_future_booking, form_time


# Create your views here.
def dashboard(request):
    drones_data = get_drones_of_user(request.session['username'])
    context = {
        "username": request.session['username'],
        "drones_data": drones_data,
    }
    return render(request, '../../drone_system/templates/drone_system/dashboard.html', context)


def book(request):
    book_status = ""
    time = ""
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            if request.POST.get("Book"):
                if form.cleaned_data['origin'] != form.cleaned_data['destination']:
                    drone = find_available_drone(form.cleaned_data['origin'])
                    if drone:
                        assign_booking(drone, form.cleaned_data['origin'], form.cleaned_data['destination'], request.session['username'])
                        book_status = "Booked"
                        form = BookForm()
                    else:
                        drone = find_earliest_drone(form.cleaned_data['origin'])
                        if drone:
                            time = drone.job_finish_time
                            request.session['drone_id'] = drone.id
                            book_status = "Later"
                        else:
                            book_status = "None"
                            form = BookForm()
                else:
                    book_status = "Same"
            elif request.POST.get("Yes"):
                create_future_booking(request.session['drone_id'], form.cleaned_data['origin'], form.cleaned_data['destination'], request.session['username'])
                book_status = "Booked"
                form = BookForm()
                del request.session['drone_id']
            elif request.POST.get("No"):
                del request.session['drone_id']
                form = BookForm()
    else:
        form = BookForm()
    context = {
        "form": form,
        "book_status": book_status,
        "time": time,
    }
    return render(request, '../../drone_system/templates/drone_system/book.html', context)


def futurebook(request):
    time_validation = ""
    booking = ""
    if request.method == "POST":
        print("I am in POST")
        form = FutureBook(request.POST)
        if form.is_valid():
            if form.cleaned_data['origin'] != form.cleaned_data['destination']:
                time = form_time(form.cleaned_data['time'])
                time_validation = True
                drone = find_available_drone(form.cleaned_data['origin'])
                if drone:
                    create_future_booking(drone.id, form.cleaned_data['origin'], form.cleaned_data['destination'], request.session['username'], time)
                    booking = "Success"
                else:
                    drone = find_earliest_drone(form.cleaned_data['origin'])
                    if drone:
                        if time > drone.job_finish_time:
                            create_future_booking(drone.id, form.cleaned_data['origin'], form.cleaned_data['destination'], request.session['username'], time)
                            booking = "Success"
                        else:
                            booking = "None"
                    else:
                        booking = "None"
            else:
                print("Origin and destination is same")
                booking = "Same"
        else:
            time_validation = False
    else:
        form = FutureBook()
    context = {
        "form": form,
        "time_validation": time_validation,
        "booking": booking,
    }
    return render(request, '../../drone_system/templates/drone_system/futurebook.html', context)


def information(request):
    drones_data = get_all_drone_data()
    context = {
        "drones_data": drones_data
    }
    return render(request, '../../drone_system/templates/drone_system/information.html', context)


def help(request):
    return render(request, '../../drone_system/templates/drone_system/help.html')


def settings(request):
    return render(request, '../../drone_system/templates/drone_system/settings.html')


def changepassword(request):
    form = ChangePassword(request.POST or None)
    status = ""
    if form.is_valid():
        if validate_password(request.session['username'], form.cleaned_data['password']):
            if form.cleaned_data['new_password'] == form.cleaned_data['repeat_password']:
                change_password(request.session['username'], form.cleaned_data['new_password'])
                status = "Changed"
            else:
                status = "Not same"
        else:
            status = "Wrong"
        form = ChangePassword()
    context = {
        "form": form,
        "status": status
    }
    return render(request, '../../drone_system/templates/drone_system/changepassword.html', context)


def deleteaccount(request):
    form = DeleteAccount(request.POST or None)
    status = ""
    if form.is_valid():
        if validate_password(request.session['username'], form.cleaned_data['password']):
            delete_account(request.session['username'])
            return redirect('/dashboard/logout')
        else:
            status = "Wrong"
        form = DeleteAccount()
    context = {
        "form": form,
        "status": status
    }
    return render(request, '../../drone_system/templates/drone_system/deleteaccount.html', context)


def logout(request):
    del request.session['username']
    return redirect('/home/')
