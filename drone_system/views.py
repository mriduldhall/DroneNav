from django.shortcuts import render
from django.shortcuts import redirect
from .forms import BookForm, ChangePassword, DeleteAccount, FutureBook
from .settings import validate_password, change_password, delete_account
from .drones import get_drones_of_user, get_all_drone_data, get_all_base_data, find_available_vehicle, assign_booking, find_earliest_vehicle, create_future_booking, form_time, get_future_bookings_of_user, same_city, check_intercity_travel, find_intercity_location


# Create your views here.
def dashboard(request):
    drones_data = get_drones_of_user(request.session['username'])
    future_booking_data = get_future_bookings_of_user(request.session['username'])
    context = {
        "username": request.session['username'],
        "drones_data": drones_data,
        "future_booking_data": future_booking_data
    }
    return render(request, '../../drone_system/templates/drone_system/dashboard.html', context)


def information(request):
    drones_data = get_all_drone_data()
    bases_data = get_all_base_data()
    context = {
        "drones_data": drones_data,
        "bases_data": bases_data,
    }
    return render(request, '../../drone_system/templates/drone_system/information.html', context)


def book(request):
    book_status = ""
    time = ""
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.cleaned_data['origin'] = str(form.cleaned_data['origin'])
            form.cleaned_data['origin'] = (form.cleaned_data['origin'].split(','))[0]
            form.cleaned_data['destination'] = str(form.cleaned_data['destination'])
            form.cleaned_data['destination'] = (form.cleaned_data['destination'].split(','))[0]
            if request.POST.get("Book"):
                if form.cleaned_data['origin'] != form.cleaned_data['destination']:
                    if same_city(form.cleaned_data['origin'], form.cleaned_data['destination']):
                        # Only Base
                        base = find_available_vehicle(form.cleaned_data['origin'], "Base")
                        if base:
                            assign_booking(base, form.cleaned_data['origin'], form.cleaned_data['destination'], request.session['username'], "Base")
                            book_status = "Booked"
                            form = BookForm()
                        else:
                            print("Next available (WIP)")
                    else:
                        # Mixed
                        if check_intercity_travel(form.cleaned_data['origin']):
                            # Drone + (Base)
                            if check_intercity_travel(form.cleaned_data['destination']):
                                # Only Drone
                                drone = find_available_vehicle(form.cleaned_data['origin'], "Drone")
                                if drone:
                                    assign_booking(drone, form.cleaned_data['origin'], form.cleaned_data['destination'], request.session['username'], "Drone")
                                else:
                                    drone = find_earliest_vehicle(form.cleaned_data['origin'], "Drone")
                                    create_future_booking(drone, form.cleaned_data['origin'], form.cleaned_data['destination'], request.session['username'], "", "Drone")
                                book_status = "Booked"
                            else:
                                # Drone + Base
                                destination_destination = find_intercity_location(form.cleaned_data['destination'])
                                drone = find_available_vehicle(form.cleaned_data['origin'], "Drone")
                                if drone:
                                    finish_time = assign_booking(drone, form.cleaned_data['origin'], destination_destination, request.session['username'], "Drone")
                                else:
                                    drone = find_earliest_vehicle(form.cleaned_data['origin'], "Drone")
                                    finish_time = create_future_booking(drone, form.cleaned_data['origin'], destination_destination, request.session['username'], "", "Drone")
                                base = find_available_vehicle(destination_destination, "Base")
                                if not base:
                                    base = find_earliest_vehicle(destination_destination, "Base")
                                create_future_booking(base, destination_destination, form.cleaned_data['destination'], request.session['username'], finish_time, "Base")
                                book_status = "Booked"
                        else:
                            # Base + Drone + (Base)
                            base = find_available_vehicle(form.cleaned_data['origin'], "Base")
                            if base:
                                origin_destination = find_intercity_location(form.cleaned_data['origin'])
                                finish_time = assign_booking(base, form.cleaned_data['origin'], origin_destination, request.session['username'], "Base")
                                drone = find_available_vehicle(origin_destination, "Drone")
                                if not drone:
                                    drone = find_earliest_vehicle(origin_destination, "Drone")
                                assert drone
                                if check_intercity_travel(form.cleaned_data['destination']):
                                    # Base + Drone
                                    create_future_booking(drone, origin_destination, form.cleaned_data['destination'], request.session['username'], finish_time, "Drone")
                                else:
                                    # Base + Drone + Base
                                    destination_destination = find_intercity_location(form.cleaned_data['destination'])
                                    finish_time = create_future_booking(drone, origin_destination, destination_destination, request.session['username'], finish_time, "Drone")
                                    base = find_available_vehicle(destination_destination, "Base")
                                    if not base:
                                        base = find_earliest_vehicle(destination_destination, "Base")
                                    assert base
                                    create_future_booking(base, destination_destination, form.cleaned_data['destination'], request.session['username'], finish_time, "Base")
                                book_status = "Booked"
                            else:
                                print("Next available (WIP)")

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
        form = FutureBook(request.POST)
        if form.is_valid():
            form.cleaned_data['origin'] = str(form.cleaned_data['origin'])
            form.cleaned_data['origin'] = (form.cleaned_data['origin'].split(','))[0]
            form.cleaned_data['destination'] = str(form.cleaned_data['destination'])
            form.cleaned_data['destination'] = (form.cleaned_data['destination'].split(','))[0]
            if form.cleaned_data['origin'] != form.cleaned_data['destination']:
                time = form_time(form.cleaned_data['time'])
                time_validation = True
                drone = find_available_vehicle(form.cleaned_data['origin'])
                if drone:
                    create_future_booking(drone.id, form.cleaned_data['origin'], form.cleaned_data['destination'], request.session['username'], time)
                    booking = "Success"
                else:
                    drone = find_earliest_vehicle(form.cleaned_data['origin'])
                    if drone:
                        if time > drone.job_finish_time:
                            create_future_booking(drone.id, form.cleaned_data['origin'], form.cleaned_data['destination'], request.session['username'], time)
                            booking = "Success"
                        else:
                            booking = "None"
                    else:
                        booking = "None"
            else:
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
